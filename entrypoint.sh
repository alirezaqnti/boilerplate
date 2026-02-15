#!/bin/sh
set -e

# Run migrations and collect static files before the main command
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

# Run the command passed to the container (defaults to CMD from Dockerfile)
exec "$@"
