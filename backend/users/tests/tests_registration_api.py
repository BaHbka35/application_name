from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from users.services import get_activation_token



data = {
    "first_name": "Sasha",
    "surname": "Kurkin",
    "username": "Luk",
    "email": "nepetr86@bk.ru",
    "password": "123456789",
    "password2": "123456789"
    }


class RegistrationAPITests(APITestCase):
    """Class for testing API witch indends fro registrate user."""

    data = data.copy()
    url = reverse('users:signup')

    def test_create_account(self):
        """Tests creating user with right fields"""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, 'Luk')
        self.assertEqual(User.objects.count(), 1)

    def test_create_account_with_defferent_passwords(self):
        """Tests creating user with defferent passwords"""
        data = self.data.copy()
        data['password2'] = 'other_password'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_account_wiht_short_password(self):
        """Tests criating user with short password."""
        data = self.data.copy()
        data['password1'] = 'short'
        data['password2'] = 'short'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_account_with_not_suitable_name(self):
        """Tests creating user with not suitabel chars in first_name."""
        data = self.data.copy()
        data["first_name"] = "234a34"
        response = self.client.post(self.url, data, format='json')

        data["first_name"] = "\\aldksjw435"
        response2 = self.client.post(self.url, data, format='json')

        data["first_name"] = '"ladjfliakdf'
        response3 = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_account_with_not_suitable_surname(self):
        """Tests creating user with not suitabel chars in surname."""
        data = self.data.copy()
        data["surname"] = "234a34"
        response = self.client.post(self.url, data, format='json')

        data["surname"] = "\\aldksjw435"
        response2 = self.client.post(self.url, data, format='json')

        data["surname"] = '"ladjfliakdf'
        response3 = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_users_with_same_email(self):
        """Tests creating user with email that already exists."""
        # First_user
        data = self.data.copy()
        self.client.post(self.url, data, format='json')
        # Second user
        data2 = {
        "first_name": "Lexa",
        "surname": "Domov",
        "username": "Lusha",
        "email": "nepetr86@bk.ru",
        "password": "123456789",
        "password2": "123456789"
        }
        response = self.client.post(self.url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_users_with_same_username(self):
        """Tests creating user with username that already exists."""
        # First_user
        data = self.data.copy()
        self.client.post(self.url, data, format='json')
        # Second user
        data2 = {
        "first_name": "Lexa",
        "surname": "Domov",
        "username": "Luk",
        "email": "otheremail@gmail.com",
        "password": "123456789",
        "password2": "123456789"
        }
        response = self.client.post(self.url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class AccountActivationAPITests(APITestCase):
    """Class for testing account activation."""
    data = data.copy()

    def setUp(self):
        """Create user for testing activation his account."""
        url = reverse('users:signup')
        self.client.post(url, self.data, format='json')

    def test_activate_account(self):
        """Tests account activation with true activation_token"""
        user = User.objects.get()
        activation_token = get_activation_token(user)
        url = reverse('users:activate_account',
                      kwargs={"id": user.id, "token": activation_token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        self.assertEqual(user.is_activated, True)

    def test_activate_account_with_wrong_token(self):
        """Tests account activation with false activation_token"""
        user = User.objects.get()
        activation_token = "aljfla8ajdklf43"
        url = reverse('users:activate_account',
                      kwargs={"id": user.id, "token": activation_token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = User.objects.get()
        self.assertEqual(user.is_activated, False)

    def test_activate_account_with_wrong_id(self):
        """Tests account activation with wrong given user id."""
        user = User.objects.get()
        activation_token = get_activation_token(user)
        url = reverse('users:activate_account',
                      kwargs={"id": 333, "token": activation_token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
