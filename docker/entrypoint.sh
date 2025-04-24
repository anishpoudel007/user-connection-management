#!/bin/bash

if [ "$1" = "gunicorn" ]; then
  echo "Waiting for postgres..."
  while ! nc -z db 5432; do
    sleep 0.1
  done
  echo "PostgreSQL started"

  echo "Running migrations..."
  python manage.py migrate
fi

# Run the passed command
exec "$@"
