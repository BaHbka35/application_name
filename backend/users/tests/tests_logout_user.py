from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from .for_tests import registrate_user, activate_user, get_auth_header


signup_data = {
    'first_name': 'Sasha',
    'surname': 'Kurkin',
    'username': 'Luk',
    'email': 'nepetr86@bk.ru',
    'password': '123456789',
    'password2': '123456789'
}

login_data = {
    'username': 'Luk',
    'password': '123456789'
}


class LogOutAPITests(APITestCase):
    """Class for testing logout user."""

    url = reverse('users:logout')

    def setUp(self):
        """Registrate, activate user."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

    def test_logout_user(self):
        """Tests log user out."""
        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)

    def test_logout_not_authenticated_user(self):
        """Tests try to log somebody out."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
