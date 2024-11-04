FROM python:3.11-alpine

MAINTAINER Shapran Taras

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev mariadb-dev # for postgres libpq-dev
# for pillow
RUN apk add --no-cache jpeg-dev zlib-dev libjpeg

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /tmp

RUN cd /tmp && pip install -r requirements.txt