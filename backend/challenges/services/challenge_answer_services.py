import os

from django.conf import settings

from challenges.models import Challenge, ChallengeMember, ChallengeAnswer

from .services import delete_existing_file


class ChallengeAnswerService:

    @classmethod
    def get_challenge_answer(cls, challenge_member: ChallengeMember, challenge: Challenge):
        """"""
        return ChallengeAnswer.objects.get_or_create(challenge_member=challenge_member,
                                                     challenge=challenge)[0]

    @classmethod
    def update_video_answer(cls, member: ChallengeMember, challenge_answer: ChallengeAnswer,
                            video_answer_file: '') -> None:
        """Updates video example for challenge."""
        directory = 'video_answers'
        file_name = f'{member.user.id}_{challenge_answer.challenge.id}.mp4'
        if challenge_answer.video_answer:
            file_path = os.path.join(settings.MEDIA_ROOT, f'{directory}/{file_name}')
            delete_existing_file(file_path)

        challenge_answer.video_answer = video_answer_file
        challenge_answer.video_answer.name = file_name
        challenge_answer.save()