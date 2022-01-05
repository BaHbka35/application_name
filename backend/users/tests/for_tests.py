from django.urls import reverse

from users.services import TokenService



def registrate_user(self, signup_data):
    """Register user and activate him."""
    url = reverse('users:signup')
    response = self.client.post(url, signup_data, format='json')
    return response


def activate_user(self, user):
    activation_token = TokenService.get_activation_token(user)
    url = reverse('users:activate_account',
                  kwargs={"id": user.id, "token": activation_token})
    response = self.client.get(url)
    return response


def login_user(self, login_data):
    url = reverse('users:login')
    response = self.client.post(url, login_data, format='json')
    return response
