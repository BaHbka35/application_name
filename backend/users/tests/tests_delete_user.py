from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

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


class DeleteUserAccountTests(APITestCase):
    """Class tests deleting user."""

    url = reverse('users:delete_user_account')

    def setUp(self):
        """Registrate, activaten user."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)


    def test_delete_user(self):
        """Check that user was deleted successfully."""
        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.delete(self.url, format='json')

        users_amount = User.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users_amount, 0)
