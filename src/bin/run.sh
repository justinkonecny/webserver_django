#!/bin/bash

PROJECT="webserver"
export DJANGO_SETTINGS_MODULE=${PROJECT}.settings

# turn on bash's job control
set -m

# check for deployment
echo "Checking for deployment..."
python3 manage.py check --deploy

# collect static files in /static_root
echo "Collecting static files..."
python manage.py collectstatic --noinput

# wait until the database is accepting connections
echo "Waiting for database connection..."
python manage.py wait_for_database

# run the database migrations
echo "Running migrations..."
python manage.py migrate

# start uwsgi
echo "Starting uwsgi..."
uwsgi --ini uwsgi.ini:dev --uid=nobody --gid=nogroup

echo "Done!"
