import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from challenges.models import Challenge
from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, \
                                         set_auth_headers

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


signup_data2 = signup_data.copy()
signup_data2['username'] = 'Petr'
signup_data2['email'] = 'petr@gmail.com'

login_data2 = login_data.copy()
login_data2['username'] = 'Petr'


datetime_now = datetime.datetime.now()
time_change = datetime.timedelta(hours=24)
finish_datetime = datetime_now + time_change
finish_datetime = finish_datetime.strftime('%Y-%m-%dT%H:%M:%S')


def create_second_user(self,):
    user = registrate_and_activate_user(signup_data2)
    return user


class CreateChallengeTests(APITestCase):
    """Class for testing creation challenges."""

    url = reverse('challenges:create_challenge')
    data = {
        'name': 'challenge_name',
        'finish_datetime': finish_datetime,
        'goal': 'make 20 pushups in 10 seconds',
        'description': 'you mush make 20 pushups in 10 seconds',
        'requirements': 'stopwatch must be seen on video',
        'bet': 50
        }

    def setUp(self):
        """Registrate, activate user."""
        registrate_and_activate_user(signup_data)

    def test_create_challenge(self):
        """Tests creating user with required fields."""
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=self.data, format='json')
        challenge = Challenge.objects.get()
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.slug, f'{user.id}_challenge_name')
        self.assertEqual(challenge.creator.username, 'Luk')

    def test_same_user_create_two_challenges_with_same_name(self):
        """Tests creating challenge with same names by same user."""
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=self.data, format='json')
        response2 = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 1)

    def test_two_user_create_challenge_with_same_name(self):
        """Tests creating challenge with same names by different users."""
        create_second_user(self)

        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=self.data, format='json')

        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)
        response2 = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(Challenge.objects.count(), 2)

    def test_creating_challenge_with_not_right_data_finish_format(self):
        """
        Tests creating challenge when
        data_finish field is not right format.
        """
        data = self.data.copy()
        data['finish_datetime'] = '2022-02-lal 18:25:43'
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)

    def test_creating_challenge_with_letter_in_bet_field(self):
        """Tests creating challenge when bet field contain letter."""
        data = self.data.copy()
        data['bet'] = '5o'
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)

    def test_creating_challenge_with_float_number_in_bet_field(self):
        """Tests creating challeng when bet_field is float number."""
        data = self.data.copy()
        data['bet'] = 50.5
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)

    def test_creating_challenge_with_not_right_finish_date(self):
        """Tests creating challenge when
        finish datetime < current datetime."""
        data = self.data.copy()
        data['finish_datetime'] = '2000-02-02 18:25:43'
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)

    def test_creating_free_challenge(self):
        """Tests creating free challenge(bet=0)."""
        data = self.data.copy()
        data['bet'] = 0
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Challenge.objects.count(), 1)













