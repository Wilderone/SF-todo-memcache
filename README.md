# Example todoapp project
Я не стал размещать проект на Heroku, вместо этого поднял его на своем сервере в докер-контейнерах, а так же поднял у себя сервер Memcached, с которым и работает джанго.

В настройках cache ссылается на локальный ip сервера.

Если вы хотите поднять проект у себя, то введите в location ip из вашего http-запроса (80.65.23.35), порт оставьте 11211.
