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


class DeleteUserAccountTests(APITestCase):
    """Class tests deleting user."""

    url = reverse('users:delete_user_account')

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)

    def test_delete_user(self):
        """Check that user was deleted successfully."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.delete(self.url, format='json')

        users_amount = User.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users_amount, 0)
