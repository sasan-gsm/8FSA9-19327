#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "Waiting for PostgreSQL to be ready..."

python << END
import os
import time
import psycopg2
import sys

timeout = 30
start = time.time()

while True:
    try:
        psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT", "5432"),
        )
        break
    except psycopg2.OperationalError as e:
        if time.time() - start > timeout:
            print("ERROR: Unable to connect to the database. Exiting.")
            sys.exit(1)
        print("Waiting for PostgreSQL...")
        time.sleep(3)
END

echo "PostgreSQL is available."

echo "Applying database migrations..."
python manage.py migrate

if [ "$CREATE_SUPERUSER" = "true" ]; then
echo "Creating superuser if it doesn't exist..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "${SUPERUSER_EMAIL}"
password = "${SUPERUSER_PASSWORD}"
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
