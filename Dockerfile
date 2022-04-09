# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /bot

RUN pip3 install

COPY . .

CMD [ "python3", "-m" , "run", "--host=0.0.0.0"]
