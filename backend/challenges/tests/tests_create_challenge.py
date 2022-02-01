import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from challenges.models import Challenge
from services_for_tests.for_tests import registrate_user, activate_user, \
                                         login_user, get_auth_headers, \
                                         set_auth_headers

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

datetime_now = datetime.datetime.now()
time_change = datetime.timedelta(hours=24)
datetime_finish = datetime_now + time_change
datetime_finish = datetime_finish.strftime('%Y-%m-%dT%H:%M:%S')


class CreateChallengeTests(APITestCase):
    """Class for testing creation challenges."""

    url = reverse('challenges:create_challenge')
    data = {
        'name': 'challenge_name',
        'date_finish': datetime_finish,
        'goal': 'make 20 pushups in 10 seconds',
        'description': 'you mush make 20 pushups in 10 seconds',
        'requirements': 'stopwatch must be seen on video',
        'bet': 50
        }

    def setUp(self):
        """Registrate, activate user."""
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

    def test_create_challenge(self):
        """Tests creating user with required fields."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.post(self.url, data=self.data, format='json')
        challenge = Challenge.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.slug, 'challenge_name')
        self.assertEqual(challenge.creator.username, 'Luk')









