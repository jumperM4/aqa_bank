#!/bin/bash

echo "Остановить docker compose"
docker compose down

echo "Docker pull все образы браузеров"

# Путь до файла
json_file="./config/browsers.json"

if [ ! -f "$json_file" ]; then
    echo "Ошибка: файл $json_file не найден!"
    exit 1
fi

if command -v jq &> /dev/null; then
    jq -r '.. | .image? // empty' "$json_file" | while read -r image; do
        if [ -n "$image" ]; then
            echo "Загрузка образа: $image"
            docker pull "$image"
        fi
    done
else
    echo "jq не найден, используем grep"
    grep -oP '"image":\s*"\K[^"]+' "$json_file" | while read -r image; do
        echo "Загрузка образа: $image"
        docker pull "$image"
    done
fi

echo "Запустить docker compose"
docker compose up -d
