from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from users.services.token_services import TokenService
from users.services.token_signature_services import TokenSignatureService

from services_for_tests.for_tests import registrate_and_activate_user, registrate_user
from services_for_tests.data_for_tests import signup_data, login_data


class LogInAPITests(APITestCase):
    """Tests loging user in."""

    url = reverse('users:login')

    def setUp(self):
        registrate_and_activate_user(signup_data)

    def test_login_with_right_data(self):
        """Tests login user with right data."""
        data = login_data.copy()
        response = self.client.post(self.url, data, format='json')
        user = User.objects.get()
        token = TokenService.get_user_auth_token(user)
        signature = TokenSignatureService.get_signature(token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('token' in response.data, True)
        self.assertEqual(response.data['token'], token)
        self.assertEqual(response.data['signature'], signature)

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
        data = {'password': '123456789'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_user_password(self):
        """Tests login user without user password."""
        data = {'username': 'Luk'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
