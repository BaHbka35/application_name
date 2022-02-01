from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from users.services.token_services import TokenService
from users.services.datetime_services import DatetimeService
from .for_tests import ForTestsDateTimeService


class AccountActivationAPITests(APITestCase):
    """Class for testing account activation."""

    data = {
        "first_name": "Sasha",
        "surname": "Kurkin",
        "username": "Luk",
        "email": "nepetr86@bk.ru",
        "password": "123456789",
        "password2": "123456789"
        }

    def setUp(self):
        """Create user for testing activation his account."""
        url = reverse('users:signup')
        self.client.post(url, self.data, format='json')

    def test_activate_account(self):
        """Tests account activation with true activation_token"""
        user = User.objects.get()
        encrypted_datetime = DatetimeService.get_encrypted_datetime()
        activation_token = TokenService.get_activation_token(
            user, encrypted_datetime)

        url = reverse('users:activate_account',
                      kwargs={'id': user.id,
                              'encrypted_datetime': encrypted_datetime,
                              'token': activation_token
                              }
                      )
        response = self.client.get(url)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.is_activated, True)

    def test_activate_account_with_wrong_token(self):
        """Tests account activation with false activation_token"""
        user = User.objects.get()
        encrypted_datetime = DatetimeService.get_encrypted_datetime()
        activation_token = "aljfla8ajdklf43"
        url = reverse('users:activate_account',
                      kwargs={'id': user.id,
                              'encrypted_datetime': encrypted_datetime,
                              'token': activation_token
                              }
                      )
        response = self.client.get(url)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.is_activated, False)

    def test_activate_account_with_wrong_id(self):
        """Tests account activation with wrong given user id."""
        user = User.objects.get()
        encrypted_datetime = DatetimeService.get_encrypted_datetime()
        activation_token = TokenService.get_activation_token(
            user, encrypted_datetime)

        url = reverse('users:activate_account',
                      kwargs={'id': 4423,
                              'encrypted_datetime': encrypted_datetime,
                              'token': activation_token
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_account_with_wrong_encrypted_date(self):
        """Tests activate account with wrong encrypted date."""
        user = User.objects.get()
        encrypted_datetime = DatetimeService.get_encrypted_datetime()
        activation_token = TokenService.get_activation_token(
            user, encrypted_datetime)

        new_encrypted_datetime = DatetimeService.get_encrypted_datetime()
        url = reverse('users:activate_account',
                      kwargs={'id': user.id,
                              'encrypted_datetime': new_encrypted_datetime,
                              'token': activation_token
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_account_with_overdue_token(self):
        """Tests activate account with overdue_token."""
        user = User.objects.get()
        encrypted_datetime = ForTestsDateTimeService.get_encrypted_datetime()
        activation_token = TokenService.get_activation_token(
            user, encrypted_datetime)

        url = reverse('users:activate_account',
                      kwargs={'id': user.id,
                              'encrypted_datetime': encrypted_datetime,
                              'token': activation_token
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




