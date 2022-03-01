python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000 & celery -A config worker -l info & celery -A config beat -l info
