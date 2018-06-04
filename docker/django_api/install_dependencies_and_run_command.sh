#!/bin/bash
set -e

# call this script like
# /install_dependencies_and_run.sh test python manage.py test
# this would first install the test.txt requirements and then execute python manage.py test
# this way, we can run e.g. CI without having to install the packages necessary for that in the image
python -m venv /app/.virtualenv
source /app/.virtualenv/bin/activate
# this allows us to run commands (after installing the provided requirements file), e.g. `python manage.py runserver`
# or `python -m flake8` by overriding the ENTRYPOINT which runs gunicorn by default to execute this script instead, for
# testing and development
pip install --cache-dir /app/.cache -r /app/meron_api/requirements/"$1".txt
exec "${@:2}"
