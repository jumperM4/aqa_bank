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
sleep 15

# Проверяем статус всех контейнеров
echo "Проверка статуса контейнеров..."
sleep 5
docker ps -a | grep infrastructure

# После ожидания готовности backend, перед запуском тестов
echo "=== Тестирование авторизации admin ==="

# Попытка создать пользователя напрямую
echo "Попытка 1: Basic auth admin:admin"
curl -v -X POST http://localhost:4111/api/v1/admin/users \
  -H "Authorization: Basic YWRtaW46YWRtaW4=" \
  -H "Content-Type: application/json" \
  -d '{"username":"testUser1234","password":"testPass123$"}' 2>&1 | grep -E "(HTTP|Authorization|401|201|403)"

echo ""
echo "Попытка 2: Без авторизации"
curl -v -X POST http://localhost:4111/api/v1/admin/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"testpass123"}' 2>&1 | grep -E "(HTTP|401|201|403)"

echo ""
echo "=== Полный Backend log после ошибки ==="
docker logs infrastructure-backend-1 2>&1 | tail -50

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
