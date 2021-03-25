#!/bin/bash
set -e

echo Using usermod to set UID to ${UID}
# this will allow mounts to work, when the user on the host system has
# a UID other than 1000
# This is not required for production but shouldn't hurt
usermod -u ${UID} django

# if we are running in development, we want Django Debug Toolbar et al
if [[ $DJANGO_DEBUG = "True" ]]
then
    pip install --no-cache-dir -r /app/meron_api/requirements/development.txt
fi

# creating and making user writable only necessary paths.
# We don't do this in the Dockerfile because we want them writable to the
# UID that the host system user uses, in case folders are mounted from the
# host system
mkdir -p /app/media /app/staticfiles
# user Django will have the correct UID already
chown -R django /app/media/ /app/staticfiles/

echo Starting normal execution as django user
echo Collecting static files
DJANGO_DEBUG=False gosu django python manage.py collectstatic --no-input

# this will execute the Docker CMD as unprivileged user
# this allows us to pass e.g. "bash", or just use the default
# CMD we specified in the Dockerfile (run gunicorn)
gosu django "$@"
