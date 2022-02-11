from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, NotConfirmedEmail
from services_for_tests.for_tests import registrate_and_activate_user, get_auth_headers, set_auth_headers
from services_for_tests.data_for_tests import signup_data, login_data


class ChangeUserEmailTests(APITestCase):
    """Class for testing changing user email address."""

    url = reverse('users:change_user_email')
    data = {
        'new_user_email': 'tochno_ne_danil@mail.ru'
    }

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

    def test_change_user_email_with_true_data(self):
        """Tests changing user email with true data"""
        response = self.client.put(self.url, data=self.data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NotConfirmedEmail.objects.get().email,
                         self.data['new_user_email'])

    def test_change_user_email_for_not_auth_user(self):
        """Tests changing email for not auth user."""
        self.client.credentials()
        response = self.client.get(self.url, data=self.data,
                                   forma='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
