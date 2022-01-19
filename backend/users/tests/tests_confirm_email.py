from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, NotConfirmedEmail
from users.services.token_services import TokenService
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


class EmailConfirmationTests(APITestCase):
    """Class for tests changing user email"""

    new_user_email = 'tochno_ne_danil@mail.ru'

    def setUp(self):
        """Registrate, activate, login, and change user email."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

        changing_email_data = {
            'new_user_email': 'tochno_ne_danil@mail.ru'
        }
        changing_email_url = reverse('users:change_user_email')

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        self.client.put(changing_email_url, data=changing_email_data, format='json')

        token = TokenService.get_email_confirmation_token(user, self.new_user_email)
        kwargs = {
            'id': user.id,
            'token': token,
        }
        self.url = reverse('users:email_confirmation', kwargs=kwargs)

    def test_confirm_user_email(self):
        """
        Checks that user email was changed and his new
        email address was deleted from temporary list.
        """
        response = self.client.get(self.url)
        user = User.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.email, self.new_user_email)
        self.assertEqual(NotConfirmedEmail.objects.count(), 0)
