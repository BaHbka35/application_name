from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, NotConfirmedEmail
from services_for_tests.for_tests import registrate_and_activate_user, get_auth_headers, set_auth_headers


signup_data = {
    "first_name": "Sasha",
    "surname": "Kurkin",
    "username": "Luk",
    "email": "nepetr86@bk.ru",
    "password": "123456789",
    }

login_data = {
    "username": "Luk",
    "password": "123456789",
    }


class ChangeUserEmailTests(APITestCase):
    """Class for testing changing user email address."""

    url = reverse('users:change_user_email')
    data = {
        'new_user_email': 'tochno_ne_danil@mail.ru'
    }

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)

    def test_change_user_email_with_true_data(self):
        """Tests changing user email with true data"""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.put(self.url, data=self.data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NotConfirmedEmail.objects.get().email,
                         self.data['new_user_email'])
