from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
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


class LogOutTests(APITestCase):
    """Class for testing logout user."""

    url = reverse('users:logout')

    def setUp(self):
        """Registrate, activate user."""
        response = registrate_user(self, signup_data)
        self.user = User.objects.get(username=response.data['username'])
        activate_user(self, self.user)

    def test_logout_user(self):
        response = login_user(self, login_data)
        user_auth_token = response.data['token']

        auth_header = 'Token ' + user_auth_token
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Token.DoesNotExist):
            token = Token.objects.get(user=self.user)

    def test_logout_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
