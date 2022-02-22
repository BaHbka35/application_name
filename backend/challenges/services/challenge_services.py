import os

from typing import Optional

from django.conf import settings

from challenges.models import Challenge
from users.models import User

from .services import delete_existing_file


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

    @classmethod
    def update_video_example(cls, user: User, challenge: Challenge,
                             video_example_file: '') -> None:
        """Updates video example for challenge."""
        directory = 'video_examples'
        file_name = f'{user.id}_{challenge.id}.mp4'
        if challenge.video_example:
            file_path = os.path.join(settings.MEDIA_ROOT, f'{directory}/{file_name}')
            delete_existing_file(file_path)

        challenge.video_example = video_example_file
        challenge.video_example.name = file_name
        challenge.save()

    @staticmethod
    def add_coins_for_challenge(challenge: Challenge, coins_amount: int) -> None:
        """Add coins to challenge balance"""
        challenge.balance.coins_amount += coins_amount
        challenge.balance.save()

    @staticmethod
    def withdraw_coins_from_challenge(challenge: Challenge, coins_amount: int) -> None:
        """withdraw coins from challenge balance."""
        challenge.balance.coins_amount -= coins_amount
        challenge.balance.save()

    @staticmethod
    def is_challenge_free(challenge: Challenge) -> bool:
        """Checks is challenge free for accept it or not."""
        return challenge.bet == 0

    @staticmethod
    def get_challenge(challenge_id: int) -> Optional[Challenge]:
        """Returns challenge object"""
        try:
            return Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return None

    @staticmethod
    def make_challenges_not_active(challenge: Challenge) -> None:
        """"""
        challenge.is_active = False
        challenge.save()







