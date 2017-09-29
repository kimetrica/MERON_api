FROM python:3.6

RUN groupadd -r django \
    && useradd -r -g django django

COPY . /app/
COPY docker/django_api/run_development_server.sh /run_development_server.sh

RUN pip install --no-cache-dir -r /app/meron_api/requirements/production.txt

RUN chmod -v 755 /run_development_server.sh

# creating and making user writable only paths that are necessary. `.virtualenv` is only necessary for development,
# but as it's not activated otherwise it doesn't hurt. `media` and `staticfiles` are created outside the `meron_api`
# app source code folder, as that path will be mounted from the host system in development and we would have to take
# care of permissions if we used subfolders of `meron_api`
RUN mkdir /app/.virtualenv
RUN mkdir /app/media
RUN mkdir /app/staticfiles
# making only the folders writable for the user that are necessary.
RUN chown -R django /app/.virtualenv/ /app/media/ /app/staticfiles/

USER django

WORKDIR /app

ENV GUNICORN_REQUEST_TIMEOUT=30

ENTRYPOINT python manage.py collectstatic --no-input && /usr/local/bin/gunicorn meron_api.wsgi -w 3 -b 0.0.0.0:5000 -t $GUNICORN_REQUEST_TIMEOUT --chdir=/app
