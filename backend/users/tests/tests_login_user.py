from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from services_for_tests.for_tests import registrate_and_activate_user, registrate_user


signup_data = {
    'first_name': 'Sasha',
    'surname': 'Kurkin',
    'username': 'Luk',
    'email': 'nepetr86@bk.ru',
    'password': '123456789',
}


class LogInAPITests(APITestCase):
    """Tests loging user in."""

    url = reverse('users:login')

    def setUp(self):
        registrate_and_activate_user(signup_data)

    def test_login_with_right_data(self):
        """Tests login user with right data."""
        data = {
            'username': 'Luk',
            'password': '123456789'
        }
        response = self.client.post(self.url, data, format='json')
        user = User.objects.get(username='Luk')
        token = Token.objects.get(user=user).key

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('token' in response.data, True)
        self.assertEqual(response.data['token'], token)

    def test_login_with_not_activate_account(self):
        """Tests login user with not activated account."""
        signup_data_local = signup_data.copy()
        signup_data_local['email'] = 'test@gmial.com'
        signup_data_local['username'] = 'username'
        registrate_user(signup_data_local)
        data = {
            'username': 'username',
            'password': '123456789'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_username(self):
        """Tests login with wrong username."""
        data = {
            'username': 'wrong_username',
            'password': '123456789'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_password(self):
        """Tests login user with wrong password."""
        data = {
            'username': 'Luk',
            'password': 'wrong_password',
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_username(self):
        """Tests login user without username."""
        data = {
            'password': '123456789'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_user_password(self):
        """Tests login user without user password."""
        data = {
            'username': 'Luk'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
