FROM python:3

ADD ./app /app

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

