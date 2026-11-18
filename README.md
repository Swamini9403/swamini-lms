# Swamini LMS — Online Learning Platform (CI/CD + Docker)

**Case Study 8** · Student: **Swamini** · PRN: **202402040005** · GitHub: [@swamini9403](https://github.com/swamini9403)

A containerised learning management system with an **Angular** frontend, a **Django REST** backend, **Redis** caching
and a **MySQL** database, run with **Docker Compose** and shipped by a **GitHub Actions** CI/CD pipeline to **AWS EC2**.

```
Browser ──▶ frontend (Angular + Nginx :80) ──/api──▶ backend (Django REST + Gunicorn :8000)
                                                        ├──▶ redis  (cache :6379, volume swamini_redis_data)
                                                        └──▶ mysql  (DB    :3306, volume swamini_mysql_data)
```

## Assignment mapping

| # | Task | Where |
|---|------|-------|
| 1 | Dockerfiles for Angular and Django | [`frontend/Dockerfile`](frontend/Dockerfile), [`backend/Dockerfile`](backend/Dockerfile) |
| 2 | Multi-container Compose setup with Redis and MySQL | [`docker-compose.yml`](docker-compose.yml) |
| 3 | Persistent volumes for MySQL | `mysql_data` → named volume `swamini_mysql_data` in [`docker-compose.yml`](docker-compose.yml) |
| 4 | Docker in GitHub Actions CI/CD | [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) |

## Run locally

```bash
cp .env.example .env            # optionally change APP_PORT / passwords
docker compose up -d --build
docker compose ps
open http://localhost           # or http://localhost:$APP_PORT
```

Useful checks:

```bash
curl http://localhost/api/health/                 # DB + cache health
curl -i http://localhost/api/courses/ | grep X-Cache   # MISS first, then HIT
docker volume inspect swamini_mysql_data          # persistent MySQL volume
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health of Django, MySQL and Redis |
| GET | `/api/stats/` | Counts (cached in Redis) |
| GET | `/api/categories/` | Course categories (cached) |
| GET | `/api/courses/?search=&category=` | Course catalog (cached, `X-Cache: HIT/MISS`) |
| GET | `/api/courses/<id>/` | Course with lessons (cached) |
| GET/POST | `/api/enrollments/` | List / create enrollments (invalidates cache) |

## CI/CD pipeline

`push` to `main` runs:

1. **Backend tests**: Django tests against MySQL 8.4 and Redis 7 service containers
2. **Frontend build**: `npm ci` + Angular production build
3. **Compose integration test**: builds both Dockerfiles, starts the 4-container stack, smoke-tests through Nginx and
   checks that MySQL data survives container re-creation
4. **Build & push**: multi-arch images to GHCR (`ghcr.io/swamini9403/swamini-lms-backend|frontend`)
5. **Deploy**: SSH to EC2, install Docker if needed, `docker compose pull && up -d`, verify `/api/health/`

### Deployment configuration (repository settings)

| Type | Name | Value |
|------|------|-------|
| Variable | `EC2_HOST` | Public IP / DNS of the EC2 instance |
| Variable | `EC2_USER` | `ubuntu` (Ubuntu) or `ec2-user` (Amazon Linux) |
| Secret | `EC2_SSH_KEY` | Contents of the instance's `.pem` private key |
| Secret | `DJANGO_SECRET_KEY` | Random string |
| Secret | `MYSQL_PASSWORD` / `MYSQL_ROOT_PASSWORD` | Database passwords |

The EC2 security group must allow inbound **TCP 22** (SSH) and **TCP 80** (HTTP).
