#!/bin/bash

# waiting for db service

while ! nc db 3306; do
  >&2 echo "mysql is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Start server
echo "Starting server"
uwsgi --ini uwsgi.ini --http-socket :8000 --enable-threads