FROM python:3.9

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY flag.txt /flag.txt
RUN chmod +x init_db.sh


COPY postgresql.conf /etc/postgresql/postgresql.conf

# Устанавливаем начальную команду
CMD service postgresql start & bash init_db.sh && python run.py

