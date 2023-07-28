# Система управления и расчёта заказов мебельного предприятия
***
Для запуска проекта нужно локально поднять Postgres, Flower, Redis

`docker-compose up -d`
```
docker run -p 6379:6379 -d redis:7.0.2
```
Создать виртуальное окружение (любым удобным вам способом)
```
mkvirtualenv calc_django
pip install -r requirements.txt
```
Далее запустить сервер Django и Celery
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

celery -A config worker -l info
celery -A config beat -l info
```

***
Главная страница доступна по ссылке

[http://127.0.0.1:8000](http://127.0.0.1:8000)
***
## TODO
- refactoring html (DRY)
- refactoring js code
- refactoring crawler tasks and handlers code (DRY, KISS) split into parts
***
