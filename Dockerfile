# Используем официальный образ Python
FROM python:3.12-alpine

# Установка зависимостей для компиляции (удалятся позже)
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Установка рабочей директории
WORKDIR /app

# Копируем файлы проекта и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Запуск Django миграций и команды запуска
CMD ["./entrypoint.sh"]
