FROM python:3.12.2-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update\
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./ requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python3", "consumer.py" ]