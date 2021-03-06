from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User, UserBalance
from services_for_tests.for_tests import registrate_and_activate_user,\
                                         get_auth_headers, set_auth_headers
from services_for_tests.data_for_tests import signup_data, login_data


class DeleteUserAccountTests(APITestCase):
    """Class tests deleting user."""

    url = reverse('users:delete_user_account')

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

    def test_delete_user(self):
        """Check that user was deleted successfully."""
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserBalance.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)

    def test_delete_not_auth_user(self):
        """Tests deleting not auth user."""
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
