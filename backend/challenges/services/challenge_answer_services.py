import os

from django.conf import settings

from challenges.models import ChallengeMember, ChallengeAnswer


class ChallengeAnswerService:

    @staticmethod
    def update_video_answer(member: ChallengeMember, challenge_answer: ChallengeAnswer,
                            video_answer_file: '') -> None:
        """Updates video example for challenge."""
        file_name = f'{member.user.id}_{challenge_answer.challenge.id}.mp4'
        if challenge_answer.video_answer:
            ChallengeAnswerService.__delete_existing_video_answer(file_name)

        challenge_answer.video_answer = video_answer_file
        challenge_answer.video_answer.name = file_name
        challenge_answer.save()

    @staticmethod
    def __delete_existing_video_answer(file_name: str) -> None:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                                   f'video_answer/{file_name}'))
        except FileNotFoundError:
            pass

    @staticmethod
    def is_video_answer_file_valid(data: dict) -> bool:
        """Validates video file."""
        if 'video_answer' not in data:
            return False
        if not data['video_answer']:
            return False
        if not data['video_answer'].name[-3:] == 'mp4':
            return False
        return True
