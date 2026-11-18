# syntax=docker/dockerfile:1
# ---------- Stage 1: build Python wheels (needs compilers for mysqlclient) ----------
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt

# ---------- Stage 2: slim runtime image ----------
FROM python:3.12-slim

LABEL org.opencontainers.image.title="swamini-lms-backend" \
      org.opencontainers.image.description="Django REST API for the Swamini LMS" \
      org.opencontainers.image.source="https://github.com/swamini9403/swamini-lms"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Only the MySQL client runtime library is needed here, not the compilers
RUN apt-get update \
 && apt-get install -y --no-install-recommends libmariadb3 \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 1000 django

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

COPY --chown=django:django . .
RUN chmod +x entrypoint.sh && DB_ENGINE=sqlite python manage.py collectstatic --noinput

USER django
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=40s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health/').status==200 else 1)"

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "lms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
