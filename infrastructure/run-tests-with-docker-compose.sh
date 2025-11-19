#!/bin/bash

# Настройки
IMAGE_NAME="jumper32/nbank-tests:latest"
TIMESTAMP=$(date +"%Y%m%d_%H%M")
TEST_OUTPUT_DIR="test-output/$TIMESTAMP"

# Создаем директорию для отчетов
mkdir -p "$TEST_OUTPUT_DIR"

# Останавливаем старые контейнеры
echo "Остановка предыдущих контейнеров..."
docker compose down

# Загружаем образы браузеров
echo "Загрузка образов браузеров..."
if [ -f "./config/browsers.json" ]; then
    # Используем sed вместо grep -P для совместимости
    sed -n 's/.*"image"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "./config/browsers.json" | while read -r image; do
        if [ -n "$image" ]; then
            echo "Загрузка: $image"
            docker pull "$image"
        fi
    done
else
    echo "Файл ./config/browsers.json не найден, пропускаем загрузку браузеров"
fi

# Загружаем образ с тестами
echo "Загрузка образа с тестами..."
docker pull "$IMAGE_NAME"

# Запускаем окружение
echo "Запуск окружения..."
docker compose up -d

# Ждем готовности
echo "Ожидание готовности сервисов..."
sleep 45

# Запуск API тестов
echo "Запуск API тестов..."
docker run --rm \
  --network nbank-network \
  -e SERVER=http://backend:4111/api \
  -e API_VERSION=//v1 \
  -e TEST_PROFILE=api \
  -v "$(pwd)/$TEST_OUTPUT_DIR":/app/logs \
  "$IMAGE_NAME"

# Запуск UI тестов
echo "Запуск UI тестов..."
docker run --rm \
  --network nbank-network \
  -e SERVER=http://backend:4111/api \
  -e API_VERSION=//v1 \
  -e UI_REMOTE_URL=http://selenoid:4444/wd/hub \
  -e UI_BASE_URL=http://nginx \
  -e TEST_PROFILE=ui \
  -v "$(pwd)/$TEST_OUTPUT_DIR":/app/logs \
  "$IMAGE_NAME"

echo "Тесты завершены. Отчеты в: $TEST_OUTPUT_DIR"
