#!/bin/bash

# Ждем запуска PostgreSQL
until pg_isready -h db -p 5432; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Выполняем команды для создания таблиц
PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB <<-EOSQL
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80)  NOT NULL,
    password VARCHAR(120) NOT NULL
);

EOSQL

