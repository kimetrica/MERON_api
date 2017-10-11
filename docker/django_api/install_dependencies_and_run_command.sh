#!/bin/bash
set -e

# call this script like
# /install_dependencies_and_run.sh test python manage.py test
python -m venv /app/.virtualenv
source /app/.virtualenv/bin/activate
# this allows us to run any command using python, e.g. `python manage.py runserver` or `python -m flake8` by providing
# it as a COMMAND to the container
pip install --no-cache -r /app/meron_api/requirements/"$1".txt
exec "${@:2}"
