from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user,\
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge

from users.models import User

from challenges.services.challenge_services import ChallengeService
from challenges.models import Challenge, ChallengeMember


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

signup_data2 = {
    'first_name': 'Sasha',
    'surname': 'Kurkin',
    'username': 'Luk2',
    'email': 'nepetr286@bk.ru',
    'password': '123456789',
}

login_data2 = {
    'username': 'Luk2',
    'password': '123456789'
}


data_for_challenge = {
    'name': 'challenge_name',
    'finish_datetime': '2023-02-02 18:25:43',
    'goal': 'make 20 pushups in 10 seconds',
    'description': 'you mush make 20 pushups in 10 seconds',
    'requirements': 'stopwatch must be seen on video',
    'bet': 50
}


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

        kwargs = {
            'challenge_id': challenge.id,
        }
        self.url = reverse('challenges:accept_challenge', kwargs=kwargs)

    def test_accept_not_free_challenge(self):
        """Tests accepting not free challenge."""
        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        amount_challenge_memebers = ChallengeMember.objects.filter(
            challenge=challenge).count()
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(amount_challenge_memebers, 2)
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

        amount_challenge_memebers = ChallengeMember.objects.filter(
            challenge=free_challenge).count()
        user2 = User.objects.get(id=self.user2.id)
        challenge = Challenge.objects.get(id=free_challenge.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(amount_challenge_memebers, 2)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 0)

    def test_accept_challenge_with_not_auth_user(self):
        """Tests accepting challenge with user that not auth."""
        self.client.credentials()
        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        amount_challenge_memebers = ChallengeMember.objects.filter(
            challenge=challenge).count()
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(amount_challenge_memebers, 1)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 50)

    def test_accept_challenge_without_enough_coins(self):
        """Tests accepting challenge when user has not enough coins."""
        self.user2.balance.coins_amount = 10
        self.user2.balance.save()

        response = self.client.get(self.url)

        challenge = Challenge.objects.get()
        amount_challenge_memebers = ChallengeMember.objects.filter(
            challenge=challenge).count()
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(amount_challenge_memebers, 1)
        self.assertEqual(user2.balance.coins_amount, 10)
        self.assertEqual(challenge.balance.coins_amount, 50)

    def test_accept_challenge_that_was_already_accepted(self):
        """
        Tests accepting challenge by user
        that have acccepted this challenge.
        """
        self.user2.balance.coins_amount = 100
        self.user2.balance.save()

        response = self.client.get(self.url)
        response2 = self.client.get(self.url)

        challenge = Challenge.objects.get()
        amount_challenge_memebers = ChallengeMember.objects.filter(
            challenge=challenge).count()
        user2 = User.objects.get(id=self.user2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(amount_challenge_memebers, 2)
        self.assertEqual(user2.balance.coins_amount, 50)
        self.assertEqual(challenge.balance.coins_amount, 100)






