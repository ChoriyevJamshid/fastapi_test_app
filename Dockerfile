FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    rust \
    cargo \
    gcc \
    musl-dev \
    postgresql-dev


COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .