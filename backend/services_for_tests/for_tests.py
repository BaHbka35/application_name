import datetime

from django.urls import reverse

from users.models import User
from users.services.datetime_services import DatetimeService


def registrate_user(signup_data: dict):
    """Register user"""
    user = User.objects.create_user(**signup_data)
    return user


def activate_user(user):
    """Activate user"""
    user.is_activated = True
    user.save()
    return user

def registrate_and_activate_user(signup_data: dict):
    user = registrate_user(signup_data)
    user = activate_user(user)
    return user


def login_user(self, login_data: dict):
    """Login user"""
    url = reverse('users:login')
    response = self.client.post(url, login_data, format='json')
    return response


def get_auth_headers(self, login_data: dict) -> tuple:
    """Returns string representation of authentication headers."""
    response = login_user(self, login_data)
    user_auth_token = response.data['token']
    signature = response.data['signature']
    return user_auth_token, signature


def set_auth_headers(self, token: str, signature: str) -> None:
    """Sets headers for authentication."""
    self.client.credentials(HTTP_TOKEN=token, HTTP_SIGNATURE=signature)


class ForTestsDateTimeService(DatetimeService):
    """
    This class needs for overwrite function of perent class.
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
