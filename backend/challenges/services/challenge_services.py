import os

from django.conf import settings

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

    @staticmethod
    def is_video_example_file_valid(data: dict) -> bool:
        """Validates video file."""
        if 'video_example' not in data:
            return False
        if not data['video_example']:
            return False
        if not data['video_example'].name[-3:] == 'mp4':
            return False
        return True

    @staticmethod
    def update_video_example(user: User, challenge: Challenge,
                             video_example_file: '') -> None:
        """Updates video example for challenge."""
        file_name = f'{user.id}_{challenge.id}.mp4'
        if challenge.video_example:
            ChallengeService.__delete_existing_video_example(file_name)

        challenge.video_example = video_example_file
        challenge.video_example.name = file_name
        challenge.save()

    @staticmethod
    def __delete_existing_video_example(file_name: str) -> None:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                                   f'video_examples/{file_name}'))
        except FileNotFoundError:
            pass

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






