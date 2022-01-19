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
    'password': '123456789',
}


class UpdateUserDataAPITests(APITestCase):
    """Class tests updating user data."""

    updating_data = {
        'first_name': 'Lexa',
        'surname': 'Abramov',
        'username': 'new_username',
        'age': 33,
        'gender': 'male',
        'training_experience': 4.5,
        'trains_now': True,
    }

    url = reverse('users:update_user_data')

    def setUp(self):
        """Registrate, activate user."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

    def test_update_user_date_without_login(self):
        """Tests update user date without login."""
        response = self.client.put(self.url, data=self.updating_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_data_with_right_data(self):
        """Tests correct updating user data with right data"""
        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=self.updating_data,
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.__check_response_data(response)
        self.__check_changes_in_user_data()

    def __check_response_data(self, response):
        self.assertEqual(response.data['first_name'], 'Lexa')
        self.assertEqual(response.data['surname'], 'Abramov')
        self.assertEqual(response.data['username'], 'new_username')
        self.assertEqual(response.data['age'], 33)
        self.assertEqual(response.data['gender'], 'male')
        self.assertEqual(response.data['training_experience'], '4.5')
        self.assertEqual(response.data['trains_now'], True)

    def __check_changes_in_user_data(self):
        user = User.objects.get()
        self.assertEqual(user.first_name, 'Lexa')
        self.assertEqual(user.surname, 'Abramov')
        self.assertEqual(user.username, 'new_username')
        self.assertEqual(user.slug, 'new_username')
        self.assertEqual(user.age, 33)
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.training_experience, 4.5)
        self.assertEqual(user.trains_now, True)

    def test_update_data_with_negative_train_exp(self):
        """Tests update user data with negative training experience."""
        data = self.updating_data.copy()
        data['training_experience'] = -4.5

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)

        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.training_experience, None)

    def test_update_data_with_negative_age(self):
        """Tests update user data with negative age."""
        data = self.updating_data.copy()
        data['age'] = -19

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.age, None)

    def test_update_data_with_incorrect_first_name(self):
        """
        Tests update user data with first_name
        that contains 'bad' symbols.
        """
        data = self.updating_data.copy()
        data['first_name'] = 'laa342:234111'

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.first_name, 'Sasha')

    def test_update_data_with_incorrect_surname(self):
        """Tests update user data with surname than contains 'bad' symbols."""
        data = self.updating_data.copy()
        data['surname'] = 'laa342:234111'

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.surname, 'Kurkin')

    def test_update_data_with_not_existing_gender(self):
        """Tests update user data with not existing gender."""
        data = self.updating_data.copy()
        data['gender'] = 'wrong'

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.gender, None)

    def test_update_data_with_existing_gender(self):
        """Tests update user data with existing gender."""
        data = self.updating_data.copy()
        data['gender'] = 'female'

        auth_header = get_auth_header(self, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(self.url, data=data, format='json')

        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.gender, 'female')
        self.assertEqual(response.data['gender'], 'female')
