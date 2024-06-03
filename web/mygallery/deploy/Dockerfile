# Устанавливаем базовый образ
FROM python:3.8-slim

# Устанавливаем PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib postgresql-client

# Создаем директорию для скриптов и копируем скрипт инициализации базы данных
RUN mkdir /docker-entrypoint-initdb.d


# Устанавливаем директорию приложения в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем файлы приложения в контейнер
COPY . .

RUN chmod +x init_db.sh
# Запускаем инициализацию базы данных и приложение
CMD service postgresql start & bash init_db.sh && python run.py

