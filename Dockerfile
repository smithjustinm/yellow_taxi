FROM python:3.9

ENV PYTHONUNBUFFERED 1
WORKDIR /app

# add the workdir to the python path
ENV PYTHONPATH=/app

# necessary to store prometheus temp files for cross process communication (e.g. gunicorn -w)
ENV prometheus_multiproc_dir=/tmp
ENV LOG_LEVEL=INFO

# https://github.com/encode/uvicorn/issues/589 uvicorn + gunicorn proxy settings
ENV FORWARDED_ALLOW_IPS="*"

# disable libeatmydata
ENV LD_PRELOAD=

# set environment
ENV RELEASE_VERSION=${RELEASE_VERSION}

RUN groupadd -r app && \
    useradd -r -g app -d /app -s /sbin/nologin -c "DockerUser" app && \
    mkdir -p /app && \
    chown -R app /app

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry==1.4.2

RUN poetry config virtualenvs.create false

EXPOSE 9000
USER app

ENTRYPOINT gunicorn -c "python:yellow_taxi_data.gunicorn_config" --preload "yellow_taxi_data.main:app"
