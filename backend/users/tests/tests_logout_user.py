from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from services_for_tests.for_tests import registrate_and_activate_user, get_auth_headers, set_auth_headers


signup_data = {
    'first_name': 'Sasha',
    'surname': 'Kurkin',
    'username': 'Luk',
    'email': 'nepetr86@bk.ru',
    'password': '123456789',
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
        registrate_and_activate_user(signup_data)

    def test_logout_user(self):
        """Tests log user out."""
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)

    def test_logout_not_authenticated_user(self):
        """Tests try to log somebody out."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)










