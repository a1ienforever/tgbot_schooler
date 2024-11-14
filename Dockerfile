# Используем официальный образ Python на основе Alpine
FROM python:3.12-alpine

# Установка зависимостей для компиляции (используем apk вместо apt-get)
RUN apk update && apk add --no-cache build-base postgresql-dev

# Установка рабочей директории
WORKDIR /app

# Копируем файлы проекта и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .


# Запуск Django миграций и команды запуска
CMD python /app/django_app.py migrate && \
    python /app/django_app.py runserver 0.0.0.0:8000 & \
    python /app/bot.py