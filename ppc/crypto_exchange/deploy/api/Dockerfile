FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY main.py /app/

COPY ./auth/ /app/auth

CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]
