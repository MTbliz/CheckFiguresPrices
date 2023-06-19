FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

WORKDIR /flask

COPY flask_requirements.txt flask_requirements.txt
RUN pip3 install -r flask_requirements.txt

COPY . .
