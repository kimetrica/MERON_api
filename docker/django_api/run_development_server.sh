#!/bin/bash
python -m venv /app/.virtualenv
source /app/.virtualenv/bin/activate
pip install --no-cache -r /app/meron_api/requirements/development.txt
python manage.py runserver_plus 0.0.0.0:8000
