#!/bin/bash

# Настройки
IMAGE_NAME="nbank-tests"
DOCKERHUB_USERNAME="jumper32"
TAG="latest"

# Полное имя образа для Docker Hub
FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "=== Docker Hub Push Script ==="

# Шаг 0: Сборка образа
echo ""
echo "[0/4] Сборка свежего образа..."
docker build -t "${IMAGE_NAME}" .

if [ $? -ne 0 ]; then
    echo "Ошибка при сборке образа!"
    exit 1
fi
echo "Образ успешно собран"

# Шаг 1: Логин в Docker Hub
echo ""
echo "[1/4] Логин в Docker Hub..."
echo "Введите ваш Docker Hub Access Token:"
read -s DOCKERHUB_TOKEN

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

if [ $? -ne 0 ]; then
    echo "Ошибка авторизации!"
    exit 1
fi

# Шаг 2: Тегирование образа
echo ""
echo "[2/4] Тегирование образа..."
echo "Локальный: ${IMAGE_NAME}"
echo "Новый тег: ${FULL_IMAGE_NAME}"

docker tag "${IMAGE_NAME}" "${FULL_IMAGE_NAME}"

# Шаг 3: Push в Docker Hub
echo ""
echo "[3/4] Отправка образа в Docker Hub..."
docker push "${FULL_IMAGE_NAME}"

if [ $? -ne 0 ]; then
    echo "Ошибка при отправке образа!"
    exit 1
fi

## Шаг 4: Logout (опционально, для безопасности)
#echo ""
#echo "[4/4] Выход из Docker Hub..."
#docker logout

echo ""
echo "Готово! Образ опубликован: ${FULL_IMAGE_NAME}"
echo "Pull команда: docker pull ${FULL_IMAGE_NAME}"
