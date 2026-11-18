from django.db import models


class Course(models.Model):
    LEVELS = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=80)
    instructor = models.CharField(max_length=120)
    level = models.CharField(max_length=20, choices=LEVELS, default="Beginner")
    duration_hours = models.PositiveIntegerField(default=1)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    duration_minutes = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} / {self.title}"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    student_name = models.CharField(max_length=120)
    student_email = models.EmailField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(fields=["course", "student_email"], name="unique_enrollment"),
        ]

    def __str__(self):
        return f"{self.student_name} -> {self.course.title}"
