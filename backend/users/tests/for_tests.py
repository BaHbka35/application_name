import datetime

from django.urls import reverse

from users.services.token_services import TokenService
from users.services.datetime_services import DatetimeService


def registrate_user(self, signup_data: dict):
    """Register user"""
    url = reverse('users:signup')
    response = self.client.post(url, signup_data, format='json')
    return response


def activate_user(self, user):
    """Activate user"""
    encrypted_datetime = DatetimeService.get_encrypted_datetime()
    activation_token = TokenService.get_activation_token(user, encrypted_datetime)
    url = reverse('users:activate_account',
                  kwargs={'id': user.id,
                          'encrypted_datetime': encrypted_datetime,
                          'token': activation_token
                          }
                  )
    response = self.client.get(url)
    return response


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
