FROM python:3.9-alpine

ENV CONFIG_PATH "cfg/main.docker.cfg"
ENV LIBRARY_PATH=/lib:/usr/lib


WORKDIR /app

RUN apk add --no-cache build-base jpeg-dev zlib-dev gcc libc-dev
RUN apk del build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


CMD [ "python", "/app/main.py" ]