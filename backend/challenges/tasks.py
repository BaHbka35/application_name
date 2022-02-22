import datetime

from config.celery import app

from .models import Challenge
from .services.challenge_services import ChallengeService


@app.task
def make_challenges_not_active():
    datetime_now = datetime.datetime.now()
    challenges = Challenge.objects.all().filter(finish_datetime__lte=datetime_now)
    for challenge in challenges:
        ChallengeService.make_challenges_not_active(challenge)
