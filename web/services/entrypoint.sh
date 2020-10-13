#!/bin/bash

# waiting for db service

sleep 8

# creating database
echo "creating database"

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Start server
echo "Starting server"
uwsgi --ini uwsgi.ini --http-socket :8000 --enable-threads