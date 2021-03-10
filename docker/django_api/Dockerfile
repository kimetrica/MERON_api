FROM tensorflow/tensorflow:2.4.1

RUN groupadd -r django \
    && useradd -r -g django django

COPY . /app/

RUN apt-get update && \
    apt-get install -y cmake \
    build-essential \
    gosu && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# https://stackoverflow.com/a/63457606
RUN pip install -U pip
RUN pip install --no-cache-dir -r /app/meron_api/requirements/production.txt

WORKDIR /app

# entrypoint scripts can be used to install development/test requirements
# and run devserver/tests
# They are not used in production
ENTRYPOINT ["/app/docker/django_api/run_django.sh"]
CMD ["/usr/local/bin/gunicorn", "meron_api.wsgi", "-w", "3", "-b", "0.0.0.0:5000", "-t", "300"]
