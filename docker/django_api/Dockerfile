FROM python:3.6

RUN groupadd -r django \
    && useradd -r -g django django

COPY . /app/

# this script can be used to install development/test requirements in a new virtualenv and run devserver/tests
# It is not used in production
COPY docker/django_api/install_dependencies_and_run_command.sh /install_dependencies_and_run_command.sh
RUN chmod -v 755 /install_dependencies_and_run_command.sh

RUN apt-get update && \
    apt-get install -y cmake \
                       build-essential && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir -r /app/meron_api/requirements/production.txt

# creating and making user writable only necessary paths. `.virtualenv` is only necessary for development,
# but as it's not activated otherwise it doesn't hurt. `media` and `staticfiles` are created outside the `meron_api`
# app source code folder, as that path will be mounted from the host system in development and we would have to take
# care of permissions (and clutter the host system's source code folder) if we used subfolders of `meron_api`
RUN mkdir /app/.virtualenv
RUN mkdir /app/media
RUN mkdir /app/staticfiles
# for pip cache, in case additional packages are installed in development/testing
# the cache is not a volume so it will persist when the container is re-used, until it's deleted
RUN mkdir /app/.cache
# making only the folders writable for the user that are necessary.
RUN chown -R django /app/.virtualenv/ /app/media/ /app/staticfiles/ /app/.cache/

USER django

WORKDIR /app

ENV GUNICORN_REQUEST_TIMEOUT=30

ENTRYPOINT python manage.py collectstatic --no-input && /usr/local/bin/gunicorn meron_api.wsgi -w 3 -b 0.0.0.0:5000 -t $GUNICORN_REQUEST_TIMEOUT --chdir=/app
