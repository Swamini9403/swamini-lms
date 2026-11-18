from rest_framework import serializers

from .models import Course, Enrollment, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "order", "summary", "video_id", "video_title", "channel"]


class CourseListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    cover_video_id = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "module_no", "title", "slug", "category", "instructor", "level",
            "duration_hours", "rating", "description", "lesson_count", "enrollment_count", "cover_video_id",
        ]

    def get_cover_video_id(self, course):
        """The first lesson's video doubles as the course thumbnail."""
        first = next((lesson for lesson in course.lessons.all() if lesson.video_id), None)
        return first.video_id if first else ""


class CourseDetailSerializer(CourseListSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ["lessons", "created_at"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course", "course_title", "student_name", "student_email", "enrolled_at"]
        # Duplicates are reported by the view as 409 Conflict instead of a generic 400
        validators = []
