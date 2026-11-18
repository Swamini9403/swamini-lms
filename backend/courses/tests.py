from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Course, Enrollment


class CourseApiTests(TestCase):
    def setUp(self):
        cache.clear()
        call_command("seed_courses", verbosity=0)
        self.client = APIClient()

    def test_health_reports_database_and_cache(self):
        res = self.client.get("/api/health/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")
        self.assertEqual(res.json()["checks"]["database"]["status"], "up")
        self.assertEqual(res.json()["checks"]["cache"]["status"], "up")

    def test_course_list_is_cached(self):
        first = self.client.get("/api/courses/")
        second = self.client.get("/api/courses/")
        self.assertEqual(first["X-Cache"], "MISS")
        self.assertEqual(second["X-Cache"], "HIT")
        self.assertEqual(len(second.json()["data"]), Course.objects.count())

    def test_search_and_category_filter(self):
        res = self.client.get("/api/courses/", {"category": "DevOps"})
        self.assertTrue(all(c["category"] == "DevOps" for c in res.json()["data"]))
        res = self.client.get("/api/courses/", {"search": "redis"})
        self.assertEqual(len(res.json()["data"]), 1)

    def test_course_detail_includes_lessons(self):
        course = Course.objects.first()
        res = self.client.get(f"/api/courses/{course.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()["data"]["lessons"]), 0)

    def test_enrollment_invalidates_cache_and_rejects_duplicates(self):
        course = Course.objects.first()
        self.client.get("/api/stats/")
        payload = {"course": course.id, "student_name": "Swamini", "student_email": "swamini@example.com"}
        self.assertEqual(self.client.post("/api/enrollments/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/enrollments/", payload, format="json").status_code, 409)
        stats = self.client.get("/api/stats/")
        self.assertEqual(stats["X-Cache"], "MISS")
        self.assertEqual(stats.json()["data"]["enrollments"], Enrollment.objects.count())
