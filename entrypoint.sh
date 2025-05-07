#!/bin/bash

# Set script to exit on any errors.
set -e

# Migration
echo "Performing database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate
echo "Database migrations completed."

# setup
# echo "Starting server..."
# python3 manage.py runserver 0.0.0.0:8000
# gunicorn --bind 0.0.0.0:8000 --workers 4 configuration.wsgi:application  --log-level=info --timeout 500
uvicorn configuration.asgi:application --host 0.0.0.0 --port 8000 --log-level=info --timeout-keep-alive 500