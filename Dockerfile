FROM python:3.9

ENV PYTHONPATH=/usr/src/app
# necessary to store prometheus temp files for cross process communication (e.g. gunicorn -w)
ENV prometheus_multiproc_dir=/tmp
# https://github.com/encode/uvicorn/issues/589 uvicorn + gunicorn proxy settings
ENV FORWARDED_ALLOW_IPS="*"

# set the workdir
WORKDIR /usr/src/app

# set environment
RUN mkdir -p .tox && \
    groupadd -r app &&\
    useradd -r -g app -d /usr/src/app -s /sbin/nologin -c "DockerUser" app && \
    mkdir -p /usr/src/app && \
    chown -R app /usr/src/app

COPY yellow_taxi_data ./yellow_taxi_data
COPY ./requirements.txt ./requirements.txt
COPY tests ./tests

RUN python -m pip install -r requirements.txt

COPY tests ./tests

# set user
USER app
