# quick_solver | easy | ppc

## Информация

> А можешь ли ТЫ решать СЛАУ в голове? \
> \
> nc ip_address 1488

## Деплой


```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание

smt solver

## Решение

Распарсить систему уравнений, решить ее через smt solver, отправить решение по формату обратно, и повторить 500 раз.

[Эксплоит](solve/solve.py)

## Флаг

`goctf{w0w_y0u_c4n_50lv3_l50f_qu173_f457}`

