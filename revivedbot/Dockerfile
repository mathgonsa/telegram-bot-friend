FROM python:3.9-alpine
ENV CONFIG_PATH "cfg/main.docker.cfg"
ENV LIBRARY_PATH=/lib:/usr/lib
RUN mkdir /code/
WORKDIR /code
ADD requirements.txt /code/
RUN apk add --no-cache build-base jpeg-dev zlib-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
RUN apk del build-base
ADD . /code/
CMD ["python", "-u", "run.py"]