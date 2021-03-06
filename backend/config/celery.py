import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make_challenges_not_active': {
        'task': 'challenges.tasks.make_challenges_not_active',
        'schedule': crontab(minute='*/1'),
    }
}
