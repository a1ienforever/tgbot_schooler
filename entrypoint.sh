#!/bin/bash

# Выполнение миграций
python .\django_app.py migrate

# Запуск сервера Django
python .\django_app.py runserver 0.0.0.0:8000 &

# Запуск Aiogram бота
python bot.py
