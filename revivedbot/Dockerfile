FROM python:3.9

ENV CONFIG_PATH "cfg/main.docker.cfg"
ENV LIBRARY_PATH=/lib:/usr/lib

# RUN apk add --no-cache build-base jpeg-dev zlib-dev gcc libc-dev
# RUN apk del build-base

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ADD .cache /root/.cache/huggingface

COPY . /app

CMD [ "python", "/app/main.py" ]