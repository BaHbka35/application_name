import datetime

from django.db.utils import IntegrityError

from challenges.models import Challenge
from users.models import User


class ChallengeService:
    """Class which contain all logic belongs to challenge"""

    @staticmethod
    def create_challenge(data: dict, user: User) -> Challenge:
        """Creates challenge"""

        challenge_name = data['name']
        challenge = Challenge(
            name=challenge_name,
            slug=f'{user.id}_{challenge_name}',
            creator=user,
            finish_datetime=data['finish_datetime'],
            goal=data['goal'],
            description=data['description'],
            requirements=data['requirements'],
            bet=data['bet'],
        )
        challenge.save()
        return challenge
