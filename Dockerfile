FROM python:3.11-alpine

WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Обновляем пакеты и устанавливаем зависимости в одном RUN
RUN apk update && apk add --no-cache \
    build-base openssl-dev libffi-dev \
    icu-libs \
    gettext \
    gcc python3 python3-dev musl-dev linux-headers \
    glib-dev \
    poppler-dev vips-dev vips-tools \
    poppler-utils ffmpeg \
    postgresql-dev

# Копируем requirements.txt и устанавливаем зависимости
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .