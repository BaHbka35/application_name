from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from users.services.token_services import ActivationTokenService
from users.services.datetime_services import DatetimeEncryptionService

from services_for_tests.for_tests import registrate_user, ForTestsDateTimeService
from services_for_tests.data_for_tests import signup_data


class AccountActivationAPITests(APITestCase):
    """Class for testing account activation."""

    def setUp(self):
        """Create user for testing activation his account."""
        registrate_user(signup_data)

    def test_activate_account(self):
        """Tests account activation with true activation_token"""
        user = User.objects.get()
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        activation_token = ActivationTokenService.get_activation_token(
            user, encrypted_datetime)

        kwargs = {'id': user.id,
                  'encrypted_datetime': encrypted_datetime,
                  'token': activation_token
                  }
        url = reverse('users:activate_account', kwargs=kwargs)
        response = self.client.get(url)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.is_activated, True)

    def test_activate_account_with_wrong_token(self):
        """Tests account activation with false activation_token"""
        user = User.objects.get()
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        activation_token = "aljfla8ajdklf43"
        kwargs = {'id': user.id,
                  'encrypted_datetime': encrypted_datetime,
                  'token': activation_token
                  }
        url = reverse('users:activate_account', kwargs=kwargs)
        response = self.client.get(url)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.is_activated, False)

    def test_activate_account_with_wrong_id(self):
        """Tests account activation with wrong given user id."""
        user = User.objects.get()
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        activation_token = ActivationTokenService.get_activation_token(
            user, encrypted_datetime)

        kwargs = {'id': 4423,
                  'encrypted_datetime': encrypted_datetime,
                  'token': activation_token
                  }
        url = reverse('users:activate_account', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_account_with_wrong_encrypted_date(self):
        """Tests activate account with wrong encrypted date."""
        user = User.objects.get()
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        activation_token = ActivationTokenService.get_activation_token(
            user, encrypted_datetime)
        new_encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()

        kwargs = {'id': user.id,
                  'encrypted_datetime': new_encrypted_datetime,
                  'token': activation_token
                  }
        url = reverse('users:activate_account', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_account_with_overdue_token(self):
        """Tests activate account with overdue_token."""
        user = User.objects.get()
        encrypted_datetime = ForTestsDateTimeService.get_encrypted_datetime()
        activation_token = ActivationTokenService.get_activation_token(
            user, encrypted_datetime)

        kwargs = {'id': user.id,
                  'encrypted_datetime': encrypted_datetime,
                  'token': activation_token
                  }
        url = reverse('users:activate_account', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




