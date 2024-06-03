# Painable | hard | pwn

## Информация

> Текст, который будет приложен к заданию
>
> Если нужно - указываем сразу строку подключения (nc или http или что-то еще)
> http://<ip>:1557

## Деплой

Указываем команду необходимую для запуска задачи на сервере

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание

Can you do anything if you cannot?

## Решение

Переполняша на стеке в проге без библиотек. Спреим на стек sigreturn frame, вызываем sigreturn syscall, дальше делаем мпротект на базу бинаря, потому что у нас нет други адресов. Туда же ставим стек, чтобы потом вернуться в мейн. Вернувшись в мейн, пишем шеллкод в наш rwx сегмент

[Эксплоит](exploit/sploit.py)

## Флаг

`goctf{516r37urn_d3l437_brrrr}`
