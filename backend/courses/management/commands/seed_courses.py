from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course, Lesson
from courses.views import bump_catalog_version

SWAMINI = "Swamini Mote"
NEHA = "Neha Shinde"
VAISHNAVI = "Vaishnavi Phad"

# Each module: (slug, title, category, curated by, level, hours, rating, description, lessons)
# Each lesson: (title, notes, YouTube video id, video title, channel)
MODULES = [
    ("docker-fundamentals", "Docker Fundamentals", "DevOps", SWAMINI, "Beginner", 6, 4.8,
     "Understand images, containers and Dockerfiles from first principles and containerise your first application.",
     [
         ("What is Docker?",
          "Docker packages an application together with its runtime, libraries and configuration into an image. "
          "A container is a running instance of that image, isolated from the host but much lighter than a virtual machine.",
          "Gjnup-PuquQ", "Docker in 100 Seconds", "Fireship"),
         ("Containers vs virtual machines",
          "Containers share the host kernel, so they start in milliseconds and use far less memory than VMs. "
          "This is why one EC2 instance can run the whole LearnSphere stack: Nginx, Django, Redis and MySQL.",
          "eGz9DS-aIeY", "you need to learn Docker RIGHT NOW!! // Docker Containers 101", "NetworkChuck"),
         ("Writing a Dockerfile",
          "A Dockerfile is a recipe of instructions (FROM, WORKDIR, COPY, RUN, CMD). Each instruction creates a cached "
          "layer, so copying dependency files before source code keeps rebuilds fast.",
          "gAkwW2tuIqE", "Learn Docker in 7 Easy Steps - Full Beginner's Tutorial", "Fireship"),
         ("Images, registries and the Docker CLI",
          "Images are built with docker build, tagged, and pushed to a registry such as Docker Hub or GitHub Container "
          "Registry. docker run, ps, logs and exec are the everyday commands for working with containers.",
          "pTFZFxd4hOI", "Docker Tutorial for Beginners", "Programming with Mosh"),
     ]),
    ("docker-compose-for-multi-container-apps", "Docker Compose for Multi-Container Apps", "DevOps", SWAMINI,
     "Intermediate", 5, 4.7,
     "Describe the Angular, Django, Redis and MySQL services in one docker-compose.yml and run them with one command.",
     [
         ("Why Docker Compose?",
          "Real applications need several containers. Compose describes services, networks and volumes in a single "
          "YAML file so the whole stack starts with docker compose up -d and stops with docker compose down.",
          "Qw9zlE3t8Ko", "Docker Compose in 12 Minutes", "Jake Wright"),
         ("Services, ports and environment variables",
          "Each service defines an image or build context, environment variables and published ports. Values such as "
          "passwords are read from a .env file so secrets never live in the compose file or in Git.",
          "HG6yIjZapSA", "Docker Compose Tutorial", "Programming with Mosh"),
         ("Healthchecks and start-up order",
          "depends_on with condition: service_healthy makes Django wait until MySQL and Redis pass their healthchecks, "
          "and makes Nginx wait for a healthy backend. This removes race conditions at start-up.",
          "DM65_JyGxCo", "Docker Compose will BLOW your MIND!! (a tutorial)", "NetworkChuck"),
         ("A complete Compose project",
          "A full walkthrough of building, running and debugging a multi-container application with Compose, "
          "including logs, rebuilding single services and cleaning up.",
          "SXwC9fSwct8", "Ultimate Docker Compose Tutorial", "TechWorld with Nana"),
     ]),
    ("docker-volumes-and-networking", "Docker Volumes, Networking and Persistence", "DevOps", VAISHNAVI,
     "Intermediate", 4, 4.8,
     "Keep MySQL data safe with named volumes and connect containers securely with user-defined networks.",
     [
         ("Docker volumes explained",
          "A container's file system disappears with the container. A named volume (swamini_mysql_data) is stored by "
          "Docker on the host, so the database survives docker compose down, image upgrades and redeployments.",
          "p2PH_YPCsis", "Docker Volumes explained in 6 minutes", "TechWorld with Nana"),
         ("Docker networking",
          "Containers on the same user-defined network reach each other by service name (backend, mysql, redis). "
          "LearnSphere uses two networks so the public Nginx container can never talk to the database directly.",
          "bKFMS5C4CG0", "Docker networking is CRAZY!! (you NEED to learn it)", "NetworkChuck"),
         ("Docker in depth",
          "A complete course covering images, containers, volumes, networks and Compose, tying all the concepts of "
          "this module together.",
          "3c-iBn73dDE", "Docker Tutorial for Beginners [FULL COURSE in 3 Hours]", "TechWorld with Nana"),
         ("Docker for development and production",
          "Using bind mounts for development, environment-specific Compose files and production-ready images.",
          "9zUHg7xjIqQ", "Learn Docker - DevOps with Node.js & Express", "freeCodeCamp.org"),
     ]),
    ("cicd-with-github-actions", "CI/CD with GitHub Actions", "DevOps", SWAMINI, "Intermediate", 7, 4.9,
     "Automate testing, Docker image builds and deployment to AWS EC2 on every push to GitHub.",
     [
         ("What is CI/CD?",
          "Continuous Integration builds and tests every change automatically; Continuous Delivery/Deployment ships "
          "the tested build to servers. Together they make releases small, frequent and safe.",
          "scEDHsr3APg", "DevOps CI/CD Explained in 100 Seconds", "Fireship"),
         ("Git essentials",
          "Commits, branches and pushes are the triggers of every pipeline. LearnSphere's workflow runs on each push "
          "and pull request to the main branch.",
          "hwP7WQkmECE", "Git Explained in 100 Seconds", "Fireship"),
         ("GitHub Actions with Docker",
          "Workflows are YAML files in .github/workflows made of jobs and steps. This lesson builds a pipeline that "
          "builds a Docker image and pushes it to a registry, exactly like LearnSphere's build-and-push job.",
          "R8_veQiYBjI", "GitHub Actions Tutorial - Basic Concepts and CI/CD Pipeline with Docker", "TechWorld with Nana"),
         ("Practical pipeline patterns",
          "Running tests, caching dependencies, using secrets and deploying automatically from GitHub Actions.",
          "eB0nUzAI7M8", "5 Ways to DevOps-ify your App - Github Actions Tutorial", "Fireship"),
     ]),
    ("angular-from-scratch", "Angular Frontend Development", "Frontend", NEHA, "Beginner", 10, 4.6,
     "Build a fast single-page application with Angular components, routing and HTTP calls to a REST API.",
     [
         ("Angular in a nutshell",
          "Angular is a TypeScript framework for single-page applications. LearnSphere's UI is built from standalone "
          "components, signals for state and the Angular router for navigation.",
          "Ata9cSC2WpM", "Angular in 100 Seconds", "Fireship"),
         ("TypeScript basics",
          "TypeScript adds static types to JavaScript. Typed interfaces such as Course and Lesson catch API mistakes "
          "at build time instead of in the browser.",
          "zQnBQ4tB3ZA", "TypeScript in 100 Seconds", "Fireship"),
         ("Components, templates and services",
          "Components own a template and logic; services such as ApiService share data access across pages and use "
          "HttpClient to call the Django REST API through Nginx.",
          "k5E2AVpwsko", "Angular Tutorial for Beginners: Learn Angular & TypeScript", "Programming with Mosh"),
         ("Building a complete Angular app",
          "A full course on routing, forms, HTTP and building for production with ng build, the command used in "
          "LearnSphere's Dockerfile.",
          "3qBXWUpoPHo", "Angular for Beginners Course [Full Front End Tutorial with TypeScript]", "freeCodeCamp.org"),
     ]),
    ("django-rest-framework", "Django REST Framework APIs", "Backend", VAISHNAVI, "Intermediate", 9, 4.7,
     "Design JSON APIs with Django and Django REST Framework, backed by MySQL and accelerated by Redis.",
     [
         ("Python refresher",
          "Django is written in Python, a readable general-purpose language. The backend container runs Python 3.12 on "
          "a slim Debian base image.",
          "x7X9w_GIm1s", "Python in 100 Seconds", "Fireship"),
         ("REST API design",
          "REST APIs expose resources (courses, lessons, enrollments) through HTTP verbs and URLs and exchange JSON. "
          "Status codes like 201 Created and 409 Conflict tell the client what happened.",
          "-MTSQjw5DrM", "RESTful APIs in 100 Seconds // Build an API from Scratch with Node.js Express", "Fireship"),
         ("Django fundamentals",
          "Models map Python classes to database tables, migrations evolve the schema and the admin site manages data. "
          "The container entrypoint runs migrate automatically on every start.",
          "rHux0gMZ3Eg", "Django Tutorial for Beginners – Build Powerful Backends", "Programming with Mosh"),
         ("Building APIs with DRF",
          "Serializers convert models to JSON and validate input; API views handle requests. LearnSphere's course "
          "views also add Redis caching with X-Cache HIT/MISS headers.",
          "c708Nf0cHrs", "Build a Django REST API with the Django Rest Framework. Complete Tutorial.", "CodingEntrepreneurs"),
         ("DRF in depth",
          "A complete course on viewsets, authentication, permissions and testing Django REST Framework APIs.",
          "tujhGdn1EMI", "Django REST Framework Course – Build Web APIs with Python", "freeCodeCamp.org"),
     ]),
    ("mysql-for-developers", "MySQL and Database Design", "Database", VAISHNAVI, "Beginner", 6, 4.5,
     "Model data with tables and relationships, write SQL queries and keep the database fast.",
     [
         ("SQL in 100 seconds",
          "SQL is the language of relational databases. MySQL 8.4 stores LearnSphere's courses, lessons and "
          "enrollments in related tables.",
          "zsjvFFKOm3c", "SQL Explained in 100 Seconds", "Fireship"),
         ("Choosing a database",
          "Relational, key-value, document and graph databases solve different problems. LearnSphere combines a "
          "relational database (MySQL) with a key-value store (Redis).",
          "W2Z7fbCLSTw", "7 Database Paradigms", "Fireship"),
         ("Writing SQL queries",
          "SELECT, JOIN, GROUP BY and aggregate functions. Django generates these queries for you, but understanding "
          "them helps when debugging inside the MySQL container.",
          "7S_tz1z_5bA", "SQL Course for Beginners [Full Course]", "Programming with Mosh"),
         ("Indexes and performance",
          "Indexes let the database find rows without scanning the whole table. Unique constraints, like the one "
          "preventing duplicate enrollments, are also backed by indexes.",
          "-qNSXK7s7_w", "Database Indexing Explained (with PostgreSQL)", "Hussein Nasser"),
     ]),
    ("redis-caching-patterns", "Redis Caching and Web Performance", "Database", NEHA, "Advanced", 4, 4.8,
     "Use Redis as a cache in front of MySQL and serve the frontend efficiently with Nginx.",
     [
         ("Redis in 100 seconds",
          "Redis is an in-memory key-value store with sub-millisecond reads, ideal for caching API responses.",
          "G1rOthIU-uo", "Redis in 100 Seconds", "Fireship"),
         ("Caching with Redis",
          "The cache-aside pattern: read from Redis first, fall back to MySQL on a miss and store the result. "
          "LearnSphere invalidates all catalogue keys at once by bumping a version number after each enrollment.",
          "jgpVdJB2sKQ", "Redis Crash Course", "Web Dev Simplified"),
         ("Redis beyond caching",
          "Data structures, persistence (AOF/RDB) and when Redis can be used as a primary database.",
          "OqCK95AS-YE", "Redis Crash Course - the What, Why and How to use Redis as your primary database",
          "TechWorld with Nana"),
         ("Nginx as web server and reverse proxy",
          "Nginx serves the compiled Angular files, compresses them with gzip and forwards /api/ requests to the "
          "Django container.",
          "JKxlsvZXG7c", "NGINX Explained in 100 Seconds", "Fireship"),
     ]),
    ("linux-and-aws-ec2-basics", "AWS EC2 and Linux for Deployment", "Cloud", NEHA, "Beginner", 5, 4.6,
     "Launch, secure and connect to an EC2 instance and run Docker workloads on Linux.",
     [
         ("AWS in 100 seconds",
          "Amazon Web Services offers on-demand compute, storage and networking. EC2 provides virtual servers billed "
          "by the second.",
          "ZzI9JE0i6Lc", "AWS for the Haters in 100 Seconds", "Fireship"),
         ("Linux essentials",
          "EC2 instances run Linux; LearnSphere uses Amazon Linux 2023. Package managers, services (systemctl) and "
          "file permissions are the basics needed to install Docker.",
          "rrB13utjYV4", "Linux in 100 Seconds", "Fireship"),
         ("EC2 instances and security groups",
          "Choosing an AMI and instance type, creating a key pair and opening ports 22 (SSH) and 80 (HTTP) in the "
          "security group.",
          "iHX-jtKIVNA", "Amazon EC2 Basics & Instances Tutorial", "Stephane Maarek"),
         ("How SSH works",
          "SSH uses public-key cryptography: the .pem private key stays with you (and in GitHub Secrets for the "
          "deploy job) while EC2 holds the public key.",
          "rlMfRa7vfO8", "How SSH Really Works", "ByteByteGo"),
         ("EC2 hands-on",
          "A complete EC2 walkthrough: launching an instance, connecting to it and hosting a web server.",
          "8TlukLu11Yo", "AWS EC2 Tutorial For Beginners | What Is AWS EC2?", "Simplilearn"),
     ]),
]


class Command(BaseCommand):
    help = "Create or update the LearnSphere modules and lessons (idempotent, keeps enrollments)."

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        for module_no, (slug, title, category, curator, level, hours, rating, description, lessons) in enumerate(MODULES, 1):
            course, is_new = Course.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    module_no=module_no, title=title, category=category, instructor=curator, level=level,
                    duration_hours=hours, rating=rating, description=description,
                ),
            )
            created += is_new
            for order, (l_title, notes, video_id, video_title, channel) in enumerate(lessons, 1):
                Lesson.objects.update_or_create(
                    course=course, order=order,
                    defaults=dict(title=l_title, summary=notes, video_id=video_id,
                                  video_title=video_title, channel=channel),
                )
            course.lessons.filter(order__gt=len(lessons)).delete()
        bump_catalog_version()
        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created} new module(s), {Course.objects.count()} total, {Lesson.objects.count()} lessons."
        ))
