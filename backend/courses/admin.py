from django.contrib import admin

from .models import Course, Enrollment, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "instructor", "level", "duration_hours")
    list_filter = ("category", "level")
    search_fields = ("title", "instructor")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_email", "course", "enrolled_at")
