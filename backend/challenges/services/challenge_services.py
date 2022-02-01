import datetime

from challenges.models import Challenge


class ChallengeService:
    """Class which contain all logic belongs to challenge"""

    @staticmethod
    def create_challenge(data, user):
        """Creates challenge"""
        data['date_finish'] = datetime.datetime.strptime(data['date_finish'],
                                                         '%Y-%m-%d %H:%M:%S')
        Challenge(
            name=data['name'],
            slug=data['name'],
            creator=user,
            date_finish=data['date_finish'],
            goal=data['goal'],
            description=data['description'],
            requirements=data['requirements'],
            bet=data['bet'],
        ).save()
