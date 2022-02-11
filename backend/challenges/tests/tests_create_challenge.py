import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from challenges.models import Challenge, ChallengeBalance, ChallengeMember
from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, \
                                         set_auth_headers
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


def get_finish_datatime():
    datetime_now = datetime.datetime.now()
    time_change = datetime.timedelta(hours=24)
    finish_datetime = datetime_now + time_change
    finish_datetime = finish_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    return finish_datetime

class CreateChallengeTests(APITestCase):
    """Class for testing creation challenges."""

    url = reverse('challenges:create_challenge')
    data = data_for_challenge.copy()
    data['finish_datetime'] = get_finish_datatime()

    def setUp(self):
        """Registrate, activate user."""
        user = registrate_and_activate_user(signup_data)
        user.balance.coins_amount = 50
        user.balance.save()
        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

    def test_create_challenge(self):
        """Tests creating user with required fields."""
        response = self.client.post(self.url, data=self.data, format='json')
        challenge = Challenge.objects.get()
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.slug, f'{user.id}_challenge_name')
        self.assertEqual(challenge.creator.username, 'Luk')
        self.assertEqual(ChallengeBalance.objects.count(), 1)
        self.assertEqual(ChallengeBalance.objects.get().challenge, challenge)
        self.assertEqual(ChallengeBalance.objects.get().coins_amount, 50)
        self.assertEqual(user.balance.coins_amount, 0)
        self.assertEqual(ChallengeMember.objects.get().user, user)
        self.assertEqual(ChallengeMember.objects.count(), 1)

    def test_create_challenge_for_not_auth_user(self):
        """Tests creating challenge of users that not auth."""
        self.client.credentials()
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

    def test_same_user_create_two_challenges_with_same_name(self):
        """Tests creating challenge with same names by same user."""
        response = self.client.post(self.url, data=self.data, format='json')
        response2 = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 1)
        self.assertEqual(ChallengeBalance.objects.count(), 1)

    def test_two_user_create_challenge_with_same_name(self):
        """Tests creating challenge with same names by different users."""
        response = self.client.post(self.url, data=self.data, format='json')

        user = registrate_and_activate_user(signup_data2)
        user.balance.coins_amount = 50
        user.balance.save()
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)
        response2 = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(Challenge.objects.count(), 2)
        self.assertEqual(ChallengeBalance.objects.count(), 2)

    def test_creating_challenge_with_not_right_data_finish_format(self):
        """
        Tests creating challenge when
        data_finish field is not right format.
        """
        data = self.data.copy()
        data['finish_datetime'] = '2022-02-lal 18:25:43'
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

    def test_creating_challenge_with_letter_in_bet_field(self):
        """Tests creating challenge when bet field contain letter."""
        data = self.data.copy()
        data['bet'] = '5o'
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

    def test_creating_challenge_with_float_number_in_bet_field(self):
        """Tests creating challenge when bet_field is float number."""
        data = self.data.copy()
        data['bet'] = 50.5
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

    def test_creating_challenge_with_not_right_finish_date(self):
        """Tests creating challenge when
        finish datetime < current datetime."""
        data = self.data.copy()
        data['finish_datetime'] = '2000-02-02 18:25:43'
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

    def test_creating_free_challenge(self):
        """Tests creating free challenge(bet=0)."""
        data = self.data.copy()
        data['bet'] = 0
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Challenge.objects.count(), 1)
        self.assertEqual(ChallengeBalance.objects.count(), 1)

    def test_creating_challenge_without_enough_coins(self):
        """Tests creating challenge when user hasn't enough coins."""
        user = User.objects.get()
        user.balance.coins_amount = 10
        user.balance.save()
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Challenge.objects.count(), 0)
        self.assertEqual(ChallengeBalance.objects.count(), 0)

















