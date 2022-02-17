from celery import Celery
from django.conf import settings

app = Celery('', broker=settings.BROKER_URL, backend=settings.BACKEND_URL,
             include=[''])
