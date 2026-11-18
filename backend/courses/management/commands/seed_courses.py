from django.core.management.base import BaseCommand
from django.utils.text import slugify

from courses.models import Course, Lesson

COURSES = [
    ("Docker Fundamentals", "DevOps", "Swamini", "Beginner", 6, 4.8,
     "Images, containers, volumes and networks explained from first principles.",
     ["What is a container?", "Writing a Dockerfile", "Layers and caching", "Volumes and bind mounts", "Container networking"]),
    ("Docker Compose for Multi-Container Apps", "DevOps", "Swamini", "Intermediate", 5, 4.7,
     "Run Angular, Django, Redis and MySQL together with one declarative file.",
     ["Compose file anatomy", "Service dependencies and healthchecks", "Named volumes", "Environment and secrets"]),
    ("CI/CD with GitHub Actions", "DevOps", "Swamini", "Intermediate", 7, 4.9,
     "Automate tests, Docker image builds and deployments on every push.",
     ["Workflows, jobs and steps", "Service containers in CI", "Building and pushing images", "Deploying to AWS EC2"]),
    ("Angular from Scratch", "Frontend", "R. Kulkarni", "Beginner", 10, 4.6,
     "Components, signals, routing and HTTP with the latest Angular.",
     ["Standalone components", "Signals and state", "Routing", "Calling REST APIs"]),
    ("Django REST Framework", "Backend", "A. Deshmukh", "Intermediate", 9, 4.7,
     "Build clean, cache-aware JSON APIs with Django and DRF.",
     ["Models and migrations", "Serializers", "Function-based API views", "Caching with Redis"]),
    ("MySQL for Developers", "Database", "P. Joshi", "Beginner", 6, 4.5,
     "Schema design, indexes and queries for application developers.",
     ["Tables and keys", "Joins", "Indexes", "Backups and persistence"]),
    ("Redis Caching Patterns", "Database", "S. Patil", "Advanced", 4, 4.8,
     "Cache-aside, versioned keys and TTL strategies for fast APIs.",
     ["Why cache?", "Cache-aside pattern", "Key versioning", "Monitoring hit ratio"]),
    ("Linux and AWS EC2 Basics", "Cloud", "M. Gokhale", "Beginner", 5, 4.6,
     "Launch, secure and manage an EC2 instance for container workloads.",
     ["Launching an instance", "Security groups", "SSH and key pairs", "Installing Docker"]),
]


class Command(BaseCommand):
    help = "Insert demo courses and lessons (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for title, category, instructor, level, hours, rating, description, lessons in COURSES:
            course, is_new = Course.objects.get_or_create(
                slug=slugify(title),
                defaults=dict(
                    title=title, category=category, instructor=instructor, level=level,
                    duration_hours=hours, rating=rating, description=description,
                ),
            )
            if is_new:
                created += 1
                Lesson.objects.bulk_create(
                    Lesson(course=course, title=t, order=i, duration_minutes=10 + 5 * i)
                    for i, t in enumerate(lessons, start=1)
                )
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} new course(s), {Course.objects.count()} total."))
