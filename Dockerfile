# Базовый образ
FROM python:3.11-slim

# Дефолтные значения аргументов
ARG TEST_PROFILE=api
ARG BACKENDURL=http://localhost:4111
ARG UI_BASE_URL=http://localhost:3000

# Переменные окружения для контейнера
ENV TEST_PROFILE=${TEST_PROFILE}
ENV BASEAPIURL=${BACKENDURL}
ENV BASEUIURL=${UI_BASE_URL}

WORKDIR /app

COPY requirements.txt .
# Загружаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь проект
COPY . .
USER root

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Bash скрипт для запуска тестов с профилем
CMD /bin/bash -c " \
    echo '>>> Running tests with profile: ${TEST_PROFILE}' ; \
    pytest -s -v -m ${TEST_PROFILE} --html=/app/logs/report.html --self-contained-html 2>&1 | tee /app/logs/run.log"