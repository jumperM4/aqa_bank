#!/bin/bash

# Настройка
IMAGE_NAME=nbank-tests
BACKEND_CONTAINER=nbank
#TIMESTAMP=$(date +"%Y%m%d_%H%M")
#TEST_OUTPUT_DIR=./test-output/$TIMESTAMP
#
## Создаем директорию для логов (если её нет)
#mkdir -p $TEST_OUTPUT_DIR
#echo "Директория для логов создана: $TEST_OUTPUT_DIR"

# Собираем Docker образ
echo "Сборка запущена"
docker build -t $IMAGE_NAME .

# Запуск контейнера с правильными переменными
#Git Bash автоматически преобразует пути, начинающиеся со слэша /, в Windows-пути, думая, что это абсолютный путь в файловой системе.
#Двойной слэш //v1 предотвращает автоматическое преобразование Git Bash.
echo "Контейнер запускается"
docker run --rm \
  --link $BACKEND_CONTAINER:backend \
  -e SERVER=http://backend:4111/api \
  -e API_VERSION=//v1 \
  -e UI_BASE_URL=http://localhost:3000 \
  -v $(pwd)/logs:/app/logs \
  $IMAGE_NAME

# Вывод итогов
echo "Тесты завершены"
#echo "Отчеты сохранены в: $TEST_OUTPUT_DIR"
