from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User, NotConfirmedEmail
from .for_tests import registrate_user, activate_user, login_user

signup_data = {
    "first_name": "Sasha",
    "surname": "Kurkin",
    "username": "Luk",
    "email": "nepetr86@bk.ru",
    "password": "123456789",
    "password2": "123456789"
    }

login_data = {
    "username": "Luk",
    "password": "123456789",
    }


class ChangePasswordTests(APITestCase):
    """Class for testing changing password."""

    url = reverse('users:change_user_email')
    data = {
        'new_user_email': 'tochno_ne_danil@mail.ru'
        }

    def setUp(self):
        """Registrate, activaten user."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

    def test_change_user_email_with_true_data(self):
        """Tests changing user email with true data"""

        response = login_user(self, login_data)
        user_auth_token = response.data['token']

        auth_header = 'Token ' + user_auth_token
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=self.data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NotConfirmedEmail.objects.get().email,
                         self.data['new_user_email'])
