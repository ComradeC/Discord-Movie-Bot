# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../requirements.txt requirements.txt

RUN apt-get update && apt-get install

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

COPY . .



