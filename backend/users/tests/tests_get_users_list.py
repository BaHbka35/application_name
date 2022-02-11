from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user, get_auth_headers, set_auth_headers
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2


class UsersListAPITests(APITestCase):
    """Tests getting list of users."""

    url = reverse('users:users_list')

    def setUp(self):
        """Registrate, activate and login first user."""
        registrate_and_activate_user(signup_data)
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

    def test_get_user_list_with_one_user(self):
        """Tests getting list of users with only one user."""
        response = self.client.get(self.url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, [
                                {
                                    'first_name': 'Sasha',
                                    'surname': 'Kurkin',
                                    'username': 'Luk'
                                },
                                ])

    def test_get_user_list_with_some_users(self):
        """Tests getting list of users with more than one user."""
        registrate_and_activate_user(signup_data2)

        response = self.client.get(self.url)
        result = [
            {
                'first_name': 'Lexa',
                'surname': 'Bubnov',
                'username': 'Lak'
            },
            {
                'first_name': 'Sasha',
                'surname': 'Kurkin',
                'username': 'Luk'
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result)

    def test_get_user_list_for_not_auth_user(self):
        """Tests getting users list for not authenticated user"""
        self.client.credentials()
        response = self.client.get(self.url,)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)









