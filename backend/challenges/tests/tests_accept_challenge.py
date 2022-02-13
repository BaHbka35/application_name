from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user,\
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge

from users.models import User

from challenges.models import Challenge, ChallengeMember


class AcceptChallengeTests(APITestCase):
    """Class for tests that test accepting challene."""

    def setUp(self):
        """Registrate, activate user and update his balance."""
        self.user = registrate_and_activate_user(signup_data)
        challenge = create_challenge(data_for_challenge, self.user)

        self.user2 = registrate_and_activate_user(signup_data2)
        self.user2.balance.coins_amount = 50
        self.user2.balance.save()

        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        kwargs = {'challenge_id': challenge.id}
        self.url = reverse('challenges:accept_challenge', kwargs=kwargs)

    def test_accept_not_free_challenge(self):
        """Tests accepting not free challenge."""
        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(challenge_members), 2)
        self.assertEqual(user2.balance.coins_amount, 0)
        self.assertEqual(challenge.balance.coins_amount, 100)

    def test_accept_free_challenge(self):
        """Tests accepting free challenge."""
        data_for_free_challenge = data_for_challenge.copy()
        data_for_free_challenge['name'] = 'second_name'
        data_for_free_challenge['bet'] = 0
        free_challenge = create_challenge(data_for_free_challenge, self.user)

        kwargs = {
            'challenge_id': free_challenge.id,
        }
        url = reverse('challenges:accept_challenge', kwargs=kwargs)

        response = self.client.get(url)

        challenge = Challenge.objects.get(id=free_challenge.id)
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(challenge_members), 2)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 0)

    def test_accept_challenge_with_not_auth_user(self):
        """Tests accepting challenge with user that not auth."""
        self.client.credentials()
        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(challenge_members), 1)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 50)

    def test_accept_challenge_without_enough_coins(self):
        """Tests accepting challenge when user has not enough coins."""
        self.user2.balance.coins_amount = 10
        self.user2.balance.save()

        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(challenge_members), 1)
        self.assertEqual(user2.balance.coins_amount, 10)
        self.assertEqual(challenge.balance.coins_amount, 50)

    def test_accept_challenge_that_was_already_accepted(self):
        """
        Tests accepting challenge by user
        that have accepted this challenge.
        """
        self.user2.balance.coins_amount = 100
        self.user2.balance.save()

        response = self.client.get(self.url)
        response2 = self.client.get(self.url)

        challenge = Challenge.objects.get()
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(challenge_members), 2)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 100)

    def test_accept_challenge_that_was_finished(self):
        """Tests accepting challenge that was finished."""
        challenge = Challenge.objects.get()
        challenge.is_active = False
        challenge.save()
        response = self.client.get(self.url)
        challenge = Challenge.objects.get()
        challenge_members = ChallengeMember.objects.filter(challenge=challenge)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(challenge_members), 1)

    def test_accept_challenge_that_does_not_exist(self):
        """Tests accepting challenge that doesn't exist"""
        kwargs = {'challenge_id': 2034}
        url = reverse('challenges:accept_challenge', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



