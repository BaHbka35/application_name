from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from services_for_tests.for_tests import registrate_and_activate_user, get_auth_headers, set_auth_headers
from services_for_tests.data_for_tests import signup_data, login_data


class ChangePasswordTests(APITestCase):
    """Class for testing changing password."""

    url = reverse('users:change_user_password')
    data = {
        'old_password': '123456789',
        'new_password': '1234567890',
        'new_password2': '1234567890',
        }

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        self.auth_headers = auth_headers

    def test_change_password(self):
        """
        Tests changing password.
        Checks that password was changed, auth token was deleted.
        Checks that users can log in with new password.
        """
        response = self.client.put(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.__check_that_password_was_changed_successfully()
        self.__check_successfully_login_with_new_password(self.auth_headers['token'])

    def __check_that_password_was_changed_successfully(self):
        """
        Checks that password was changed
        correctly and auth token was deleted.
        """
        user = User.objects.get(username="Luk")
        self.assertEqual(user.check_password(
                         self.data['old_password']), False)
        self.assertEqual(user.check_password(
                         self.data['new_password']), True)
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)

    def __check_successfully_login_with_new_password(self, user_auth_token):
        """Check that user can log in with new password."""
        new_login_data = {
            'username': 'Luk',
            'password': '1234567890',
            }
        self.client.credentials()
        url = reverse('users:login')
        response = self.client.post(url, new_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_user_auth_token = response.data['token']
        self.assertNotEqual(user_auth_token, new_user_auth_token)

    def test_change_password_for_not_auth_user(self):
        """Tests changing password for user that didn't auth."""
        self.client.credentials()
        response = self.client.get(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_new_password_not_equal_new_password2(self):
        """
        Tests changing password when input data not correct.
        new password != new password2.
        """
        data = {
            'old_password': '123456789',
            'new_password': 'first_password',
            'new_password2': 'second_password'
            }

        response = self.client.put(self.url, data=data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_new_password(self):
        """
        Tests changing password on password
        witch length smaller than 8 chars.
        """
        data = {
            'old_password': '123456789',
            'new_password': 'short',
            'new_password2': 'second_password',
            }

        data2 = {
            'old_password': '123456789',
            'new_password': 'first_password',
            'new_password2': 'short',
            }
        response = self.client.put(self.url, data=data,
                                   format='json')
        response2 = self.client.put(self.url, data=data2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)








