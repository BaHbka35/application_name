import datetime

from users.models import User
from users.services.datetime_services import DatetimeService
from users.services.token_services import TokenService
from users.services.token_signature_services import TokenSignatureService


def registrate_user(signup_data: dict) -> User:
    """Register user"""
    user = User.objects.create_user(**signup_data)
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
