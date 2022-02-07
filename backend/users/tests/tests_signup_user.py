from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User, UserBalance


class SignUpAPITests(APITestCase):
    """Class for testing API witch intends for registrate user."""

    data = {
        'first_name': 'Sasha',
        'surname': 'Kurkin',
        'username': 'Luk',
        'email': 'nepetr86@bk.ru',
        'password': '123456789',
        'password2': '123456789'
    }
    url = reverse('users:signup')

    def test_create_account(self):
        """Tests creating user with right fields."""
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, 'Luk')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual('password' in response.data, False)

        self.assertEqual(UserBalance.objects.get().user, User.objects.get())
        self.assertEqual(UserBalance.objects.count(), 1)

    def test_create_account_with_different_passwords(self):
        """Tests creating user with different passwords."""
        data = self.data.copy()
        data['password2'] = 'other_password'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        self.assertEqual(UserBalance.objects.count(), 0)

    def test_create_account_with_short_password(self):
        """Tests creating user with short password."""
        data = self.data.copy()
        data['password1'] = 'short'
        data['password2'] = 'short'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        self.assertEqual(UserBalance.objects.count(), 0)

    def test_create_account_with_not_suitable_name(self):
        """Tests creating user with not suitable chars in first_name."""
        data = self.data.copy()
        data['first_name'] = '234a34'
        response = self.client.post(self.url, data, format='json')

        data['first_name'] = '\\aldksjw435'
        response2 = self.client.post(self.url, data, format='json')

        data['first_name'] = '"ladjfliakdf'
        response3 = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserBalance.objects.count(), 0)

    def test_create_account_with_not_suitable_surname(self):
        """Tests creating user with not suitable chars in surname."""
        data = self.data.copy()
        data['surname'] = '234a34'
        response = self.client.post(self.url, data, format='json')

        data['surname'] = '\\aldksjw435'
        response2 = self.client.post(self.url, data, format='json')

        data['surname'] = '"ladjfliakdf'
        response3 = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserBalance.objects.count(), 0)

    def test_create_users_with_same_email(self):
        """Tests creating user with email that already exists."""
        # First_user
        data = self.data.copy()
        self.client.post(self.url, data, format='json')
        # Second user
        data2 = {
            'first_name': 'Lexa',
            'surname': 'Domov',
            'username': 'Lusha',
            'email': 'nepetr86@bk.ru',
            'password': '123456789',
            'password2': '123456789'
        }
        response = self.client.post(self.url, data2, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserBalance.objects.count(), 1)

    def test_create_users_with_same_username(self):
        """Tests creating user with username that already exists."""
        # First_user
        data = self.data.copy()
        self.client.post(self.url, data, format='json')
        # Second user
        data2 = {
            'first_name': 'Lexa',
            'surname': 'Domov',
            'username': 'Luk',
            'email': 'otheremail@gmail.com',
            'password': '123456789',
            'password2': '123456789'
        }
        response = self.client.post(self.url, data2, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserBalance.objects.count(), 1)

    def test_create_users_without_some_field(self):
        """Tests creating user without some field."""
        data = self.data.copy()
        del data['first_name']
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserBalance.objects.count(), 0)
