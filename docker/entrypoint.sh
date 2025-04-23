#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn --workers $(nproc) project.wsgi:application --bind 0.0.0.0:8000
