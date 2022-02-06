from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

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

signup_data2 = {
    'first_name': 'Lexa',
    'surname': 'Bubnov',
    'username': 'Lak',
    'email': 'Lexa86@bk.ru',
    'password': '123456789',
    }


class UsersListAPITests(APITestCase):
    """Tests getting list of users."""

    url = reverse('users:users_list')

    def setUp(self):
        """Registrate, activate and login first user."""
        registrate_and_activate_user(signup_data)

    def test_get_user_list_with_one_user(self):
        """Tests getting list of users with only one user."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.get(self.url)
        data = response.data
        self.assertEqual(data, [
                                {
                                    'first_name': 'Sasha',
                                    'surname': 'Kurkin',
                                    'username': 'Luk'
                                },
                                ])

    def test_get_user_list_with_some_users(self):
        """Tests getting list of users with more than one user."""
        registrate_and_activate_user(signup_data2)

        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.get(self.url)
        data = response.data
        self.assertEqual(data, [
                                {
                                    'first_name': 'Lexa',
                                    'surname': 'Bubnov',
                                    'username': 'Lak'
                                },
                                {
                                    'first_name': 'Sasha',
                                    'surname': 'Kurkin',
                                    'username': 'Luk'
                                },
                                ])

    def test_get_user_list_for_not_auth_user(self):
        response = self.client.get(self.url,)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)









