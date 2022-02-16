1. Go to backend directory

create .env and write into next.
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME='some_db_name'
DB_USER='some_user_name'
DB_USER_PASSWORD='some_db_password'
DB_HOST=db this is name of docker container
DB_PORT=5432

POSTGRES_DB='some_db_name'
POSTGRES_USER='some_user_name'
POSTGRES_PASSWORD='some_db_password'

EMAIL_USE_TLS=True
EMAIL_HOST=smtp.mail.ru
EMAIL_HOST_USER=you_mail@xxx.xx
EMAIL_HOST_PASSWORD='some_passwor'
EMAIL_PORT=2525 for example
```

Then execute next commands:
1. docker-compose build
2. docker-compose up

For testing application you can use next command:
> sudo docker exec drf_application python manage.py test
 
!!! But before this you should create /media/test/video_source/ directory and
insert in this directory video file '111.mp4'. This is needed only for tests