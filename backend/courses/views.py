import socket
import time

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, connection
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course, Enrollment, Lesson
from .serializers import CourseDetailSerializer, CourseListSerializer, EnrollmentSerializer

CATALOG_VERSION_KEY = "catalog:version"


def catalog_version():
    """Bumping this number invalidates every cached catalog response at once."""
    return cache.get_or_set(CATALOG_VERSION_KEY, 1, None)


def bump_catalog_version():
    try:
        cache.incr(CATALOG_VERSION_KEY)
    except ValueError:
        cache.set(CATALOG_VERSION_KEY, 2, None)


def cached_response(key, build):
    """Serve `build()` from Redis when possible and report HIT/MISS to the client."""
    started = time.perf_counter()
    data = cache.get(key)
    state = "HIT"
    if data is None:
        state = "MISS"
        data = build()
        cache.set(key, data)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return Response(
        {"cache": state, "elapsed_ms": elapsed_ms, "data": data},
        headers={"X-Cache": state, "X-Response-Time-ms": str(elapsed_ms)},
    )


def annotated_courses():
    return Course.objects.annotate(
        lesson_count=Count("lessons", distinct=True),
        enrollment_count=Count("enrollments", distinct=True),
    ).prefetch_related("lessons").order_by("module_no", "id")  # Meta.ordering is skipped for GROUP BY


@api_view(["GET"])
def course_list(request):
    search = request.query_params.get("search", "").strip()
    category = request.query_params.get("category", "").strip()
    key = f"courses:v{catalog_version()}:list:{category.lower()}:{search.lower()}"

    def build():
        qs = annotated_courses()
        if category:
            qs = qs.filter(category__iexact=category)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(instructor__icontains=search))
        return CourseListSerializer(qs, many=True).data

    return cached_response(key, build)


@api_view(["GET"])
def course_detail(request, pk):
    key = f"courses:v{catalog_version()}:detail:{pk}"

    def build():
        course = get_object_or_404(annotated_courses(), pk=pk)
        return CourseDetailSerializer(course).data

    return cached_response(key, build)


@api_view(["GET"])
def categories(request):
    key = f"courses:v{catalog_version()}:categories"
    return cached_response(
        key,
        lambda: list(Course.objects.order_by("category").values_list("category", flat=True).distinct()),
    )


@api_view(["GET", "POST"])
def enrollments(request):
    if request.method == "GET":
        recent = Enrollment.objects.select_related("course")[:20]
        return Response(EnrollmentSerializer(recent, many=True).data)

    serializer = EnrollmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    course = serializer.validated_data["course"]
    email = serializer.validated_data["student_email"]
    duplicate = Response(
        {"detail": "This email is already enrolled in the course."},
        status=status.HTTP_409_CONFLICT,
    )
    if Enrollment.objects.filter(course=course, student_email__iexact=email).exists():
        return duplicate
    try:
        serializer.save()
    except IntegrityError:
        return duplicate
    bump_catalog_version()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def stats(request):
    key = f"courses:v{catalog_version()}:stats"
    return cached_response(
        key,
        lambda: {
            "courses": Course.objects.count(),
            "lessons": Lesson.objects.count(),
            "enrollments": Enrollment.objects.count(),
            "categories": Course.objects.values("category").distinct().count(),
        },
    )


@api_view(["GET"])
def health(request):
    checks = {}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT sqlite_version()" if connection.vendor == "sqlite" else "SELECT VERSION()")
            checks["database"] = {"status": "up", "engine": connection.vendor, "version": cursor.fetchone()[0]}
    except Exception as exc:  # noqa: BLE001 - report any DB failure as "down"
        checks["database"] = {"status": "down", "error": str(exc)}

    try:
        cache.set("health:ping", "pong", 10)
        ok = cache.get("health:ping") == "pong"
        backend = settings.CACHES["default"]["BACKEND"].rsplit(".", 1)[-1]
        checks["cache"] = {"status": "up" if ok else "down", "backend": backend}
    except Exception as exc:  # noqa: BLE001
        checks["cache"] = {"status": "down", "error": str(exc)}

    healthy = all(c["status"] == "up" for c in checks.values())
    return Response(
        {
            "status": "healthy" if healthy else "degraded",
            "service": "swamini-lms-backend",
            "version": settings.APP_VERSION,
            "container": socket.gethostname(),
            "checks": checks,
        },
        status=status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
    )
