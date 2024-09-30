FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python", "/app/main.py" ]