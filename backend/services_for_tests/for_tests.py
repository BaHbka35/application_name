import os
import shutil
import datetime

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User, UserBalance
from users.services.datetime_services import DatetimeService
from users.services.token_services import TokenService
from users.services.token_signature_services import TokenSignatureService

from challenges.models import Challenge, ChallengeBalance, ChallengeMember
from challenges.services.challenge_services import ChallengeService


def registrate_user(signup_data: dict) -> User:
    """Register user"""
    user = User.objects.create_user(**signup_data)
    UserBalance(user=user).save()
    return user


def activate_user(user: User):
    """Activate user"""
    user.is_activated = True
    user.save()
    return user


def registrate_and_activate_user(signup_data: dict) -> User:
    """Registers and activates user"""
    user = registrate_user(signup_data)
    user = activate_user(user)
    return user


def get_auth_headers(login_data: dict) -> dict:
    """Returns dict with authentication headers."""
    user = User.objects.get(username=login_data['username'])
    token = TokenService.get_user_auth_token(user)
    signature = TokenSignatureService.get_signature(token)
    data = {'token': token, 'signature': signature}
    return data


def set_auth_headers(self, data: dict) -> None:
    """Sets headers for authentication."""
    self.client.credentials(HTTP_TOKEN=data['token'], HTTP_SIGNATURE=data['signature'])


def create_challenge(data: dict, user: User) -> Challenge:
    """Creates challenge."""
    challenge = ChallengeService.create_challenge(data, user)
    ChallengeBalance(challenge=challenge, coins_amount=challenge.bet).save()
    ChallengeMember(user=user, challenge=challenge).save()
    return challenge

def accept_challenge(user: User, challenge: Challenge) -> ChallengeMember:
    """creates challenge member."""
    challenge_member = ChallengeMember(user=user, challenge=challenge).save()
    ChallengeService.add_coins_for_challenge(challenge, challenge.bet)
    return challenge_member


def upload_video_for_challenge(user: User, challenge: Challenge,
                               MEDIA_ROOT: str):
    """Upload video for challenge."""
    file_path = os.path.join(MEDIA_ROOT, 'video_source/111.mp4')

    file = File(open(file_path, 'rb'))
    uploaded_file = SimpleUploadedFile('111.mp4', file.read(),
                                       content_type='multipart/form-data')
    ChallengeService.update_video_example(user, challenge, uploaded_file)


def clear_directory(directory: str) -> None:
    """Clear directory."""
    try:
        os.makedirs(directory)
    except:
        shutil.rmtree(directory)
        os.makedirs(directory)


class ForTestsDateTimeService(DatetimeService):
    """
    This class needs for overwrite function of parent class.
    This is need for tests. For tests with overdue token.
    """

    @classmethod
    def get_encrypted_datetime(cls) -> str:
        """
        Returned value of this function will be used for
        creating overdue token. Return encrypted datetime
        in str representation.
        """
        datetime_obj_now = datetime.datetime.now()

        time_change = datetime.timedelta(hours=25)
        new_time = datetime_obj_now - time_change

        datetime_str_now = new_time.strftime("%Y-%m-%d %H:%M:%S")

        forming_str = datetime_str_now.encode()
        encrypted_datetime = cls.fernet.encrypt(forming_str)

        return encrypted_datetime.decode()
