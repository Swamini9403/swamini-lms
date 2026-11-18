#!/bin/sh
set -e

# Wait until MySQL accepts connections (depends_on healthcheck covers most cases,
# this guards against restarts and slow first-time initialisation).
if [ "${DB_ENGINE:-mysql}" = "mysql" ]; then
  echo "Waiting for MySQL at ${MYSQL_HOST:-mysql}:${MYSQL_PORT:-3306} ..."
  python - <<'EOF'
import os, sys, time
import MySQLdb
for attempt in range(60):
    try:
        MySQLdb.connect(
            host=os.getenv("MYSQL_HOST", "mysql"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "lms_user"),
            password=os.getenv("MYSQL_PASSWORD", "lms_password"),
            database=os.getenv("MYSQL_DATABASE", "lms"),
        ).close()
        print("MySQL is ready.")
        sys.exit(0)
    except Exception as exc:
        print(f"  attempt {attempt + 1}: {exc}")
        time.sleep(2)
sys.exit("MySQL did not become ready in time")
EOF
fi

python manage.py migrate --noinput
python manage.py seed_courses

exec "$@"
