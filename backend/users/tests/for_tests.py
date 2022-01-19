from django.urls import reverse

from users.services.token_services import TokenService


def registrate_user(self, signup_data: dict):
    """Register user"""
    url = reverse('users:signup')
    response = self.client.post(url, signup_data, format='json')
    return response


def activate_user(self, user):
    """Activate user"""
    activation_token = TokenService.get_activation_token(user)
    url = reverse('users:activate_account',
                  kwargs={"id": user.id, "token": activation_token})
    response = self.client.get(url)
    return response


def login_user(self, login_data: dict):
    """Login user"""
    url = reverse('users:login')
    response = self.client.post(url, login_data, format='json')
    return response


def get_auth_header(self, login_data: dict) -> str:
    """Returns string representation of authentication header."""
    response = login_user(self, login_data)
    user_auth_token = response.data['token']
    return 'Token ' + user_auth_token
