1. Go to backend directory

create .env and write into next.
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=some_db_name
DB_USER=some_user_name
DB_USER_PASSWORD=some_db_password
#db - name of docker container with postgresql
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=some_db_name
POSTGRES_USER=some_user_name
POSTGRES_PASSWORD=some_db_password

EMAIL_USE_TLS=True
EMAIL_HOST=smtp.mail.ru
EMAIL_HOST_USER=you_mail@xxx.xx
EMAIL_HOST_PASSWORD=some_password
EMAIL_PORT=2525 for example

# django superuser settings.
DJANGO_SUPERUSER_FIRST_NAME=admin
DJANGO_SUPERUSER_SURNAME=admin
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@gmail.com
DJANGO_SUPERUSER_PASSWORD=1

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379 
```

!!! You should change some settings for yourself

Then execute next commands:
1. docker-compose build
2. docker-compose up

SUPERUSER will be crated automatticaly when you execute command 'docker-compose up'.

For testing application you can use next command:
> sudo docker exec drf_application python manage.py test
 
!!! But before this you should create /media/test/video_source/ directory and
insert in this directory video file '111.mp4'. This is needed only for tests