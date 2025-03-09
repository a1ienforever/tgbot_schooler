#!/bin/bash

set -e  # Скрипт завершится, если произойдет ошибка

echo "Сохраняем изменения..."
git stash

echo "Обновляем код из репозитория..."
if git pull; then
    echo "Применяем сохраненные изменения..."
    git stash pop || echo "Нет сохраненных изменений или возник конфликт."
else
    echo "Ошибка при git pull. Прерывание."
    exit 1
fi

echo "Останавливаем контейнеры..."
docker compose down || docker-compose down

echo "Запускаем контейнеры с пересборкой..."
docker compose up -d --no-deps --build || docker-compose up -d --no-deps --build

echo "✅ Готово!"
