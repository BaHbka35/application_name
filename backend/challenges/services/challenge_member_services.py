from typing import Optional

from users.models import User
from challenges.models import Challenge, ChallengeMember


class ChallengeMemberService:

    @staticmethod
    def get_challenge_member(user: User, challenge: Challenge
                             ) -> Optional[ChallengeMember]:
        """Returns challenge_member object"""
        try:
            return ChallengeMember.objects.get(user=user, challenge=challenge)
        except ChallengeMember.DoesNotExist:
            return None

    @staticmethod
    def has_user_already_accepted_this_challenge(user: User,
                                                 challenge: Challenge) -> bool:
        """Checks has user already accepted this challenge"""
        challenge_member = ChallengeMember.objects.all().filter(
            user=user, challenge=challenge)
        return True if challenge_member else False
