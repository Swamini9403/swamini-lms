from django.contrib import admin

from .models import Course, Enrollment, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    fields = ("order", "title", "summary", "video_id", "video_title", "channel")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("module_no", "title", "category", "instructor", "level", "duration_hours")
    list_filter = ("category", "level")
    search_fields = ("title", "instructor")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_email", "course", "enrolled_at")
