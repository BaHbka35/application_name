import os

from typing import Optional

from django.conf import settings
from django.db.models.query import QuerySet

from challenges.models import Challenge, ChallengeMember, ChallengeAnswer

from .services import delete_existing_file


class ChallengeAnswerService:
    """Contains logic for challenge answers."""

    @classmethod
    def get_challenge_answer(cls, challenge_member: ChallengeMember,
                             challenge: Challenge) -> ChallengeAnswer:
        """Returns answer which was added for challenge."""
        return ChallengeAnswer.objects.get_or_create(
            challenge_member=challenge_member, challenge=challenge)[0]

    @classmethod
    def update_video_answer(cls, member: ChallengeMember,
                            challenge_answer: ChallengeAnswer,
                            video_answer_file: '') -> None:
        """Updates video answer for challenge."""
        directory = settings.CHALLENGE_ANSWERS_DIR
        file_name = f'{member.user.id}_{challenge_answer.challenge.id}.mp4'
        if challenge_answer.video_answer:
            file_path = os.path.join(settings.MEDIA_ROOT,
                                     f'{directory}/{file_name}')
            delete_existing_file(file_path)

        challenge_answer.video_answer = video_answer_file
        challenge_answer.video_answer.name = file_name
        challenge_answer.save()

    @classmethod
    def get_challenge_answer_by_current_user(
            cls, challenge: Challenge, challenge_member: ChallengeMember
            ) -> Optional[ChallengeAnswer]:
        """Returns challenge answer that belongs to current member."""
        challenge_answer = ChallengeAnswer.objects.filter(
            challenge=challenge, challenge_member=challenge_member)
        if challenge_answer:
            return challenge_answer
        return None

    @classmethod
    def get_challenge_answers(cls, challenge: Challenge,
                              challenge_member: ChallengeMember) -> Optional[QuerySet]:
        """
        If challenge is active returns only answer that belongs
        to current member else return all answers of challenge
        """
        if challenge.is_active:
            user_challenge_answer = cls.get_challenge_answer_by_current_user(
                challenge=challenge, challenge_member=challenge_member)
            return user_challenge_answer
        all_challenge_answers = ChallengeAnswer.objects.filter(challenge=challenge)
        return all_challenge_answers






