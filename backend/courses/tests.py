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

    def test_course_detail_includes_lessons_with_videos(self):
        course = Course.objects.first()
        res = self.client.get(f"/api/courses/{course.id}/")
        self.assertEqual(res.status_code, 200)
        lessons = res.json()["data"]["lessons"]
        self.assertGreater(len(lessons), 0)
        for lesson in lessons:
            self.assertRegex(lesson["video_id"], r"^[A-Za-z0-9_-]{11}$")
            self.assertTrue(lesson["summary"])

    def test_modules_are_ordered_and_curated_by_team(self):
        # Give the first-created course the highest module number: it must now be listed last
        Course.objects.filter(pk=Course.objects.order_by("id").first().pk).update(module_no=99)
        cache.clear()
        data = self.client.get("/api/courses/").json()["data"]
        self.assertEqual([c["module_no"] for c in data], sorted(c["module_no"] for c in data))
        self.assertEqual(data[-1]["module_no"], 99)
        self.assertEqual({c["instructor"] for c in data}, {"Swamini Mote", "Neha Shinde", "Vaishnavi Phad"})
        self.assertTrue(all(c["cover_video_id"] for c in data))

    def test_seed_is_idempotent(self):
        lessons = Course.objects.first().lessons.count()
        call_command("seed_courses", verbosity=0)
        self.assertEqual(Course.objects.first().lessons.count(), lessons)

    def test_enrollment_invalidates_cache_and_rejects_duplicates(self):
        course = Course.objects.first()
        self.client.get("/api/stats/")
        payload = {"course": course.id, "student_name": "Swamini", "student_email": "swamini@example.com"}
        self.assertEqual(self.client.post("/api/enrollments/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/enrollments/", payload, format="json").status_code, 409)
        stats = self.client.get("/api/stats/")
        self.assertEqual(stats["X-Cache"], "MISS")
        self.assertEqual(stats.json()["data"]["enrollments"], Enrollment.objects.count())
