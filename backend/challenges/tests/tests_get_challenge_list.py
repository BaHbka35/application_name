from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, accept_challenge
from services_for_tests.data_for_tests import signup_data, login_data,\
                                              signup_data2, login_data2,\
                                              data_for_challenge


class GetChallengesList(APITestCase):
    """
    Class which contain tests for
    testing getting challenges list.
    """

    def setUp(self):
        self.user = registrate_and_activate_user(signup_data)
        self.challenge = create_challenge(data_for_challenge, self.user)

        self.user2 = registrate_and_activate_user(signup_data2)

        self.url = reverse('challenges:get_challenges_list')

    def test_getting_challenges_list_with_one_challenge(self):
        """Tests getting challenges list when there is only one challenge."""
        response = self.client.get(self.url)
        expected_data = [{
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'members_amount': 1,
            'bet': self.challenge.bet,
            'bets_sum': 50,
            'finish_datetime': self.challenge.finish_datetime
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_getting_challenges_list_with_one_challenge_and_two_members(self):
        """
        Tests getting challenges list when there
        is only one challenge with two members.
        """
        accept_challenge(self.user2, self.challenge)
        response = self.client.get(self.url)
        expected_data = [{
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'members_amount': 2,
            'bet': self.challenge.bet,
            'bets_sum': 100,
            'finish_datetime': self.challenge.finish_datetime
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_getting_challenges_list_with_two_challenges(self):
        """
        Tests getting challenges list when there are two
        challenges and one challenge has two members.
        """
        accept_challenge(self.user2, self.challenge)
        challenge2 = create_challenge(data_for_challenge, self.user2)

        response = self.client.get(self.url)
        expected_data = [
            {
                'challenge_id': self.challenge.id,
                'name': self.challenge.name,
                'creator': self.user.username,
                'goal': self.challenge.goal,
                'members_amount': 2,
                'bet': self.challenge.bet,
                'bets_sum': 100,
                'finish_datetime': self.challenge.finish_datetime
            },
            {
                'challenge_id': challenge2.id,
                'name': challenge2.name,
                'creator': self.user2.username,
                'goal': challenge2.goal,
                'members_amount': 1,
                'bet': self.challenge.bet,
                'bets_sum': 50,
                'finish_datetime': self.challenge.finish_datetime
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_getting_challenges_list_with_two_challenges_with_one_finished(self):
        """
        Tests getting challenges lsit when there
        are two challenges and one is finished.
        """
        accept_challenge(self.user2, self.challenge)
        challenge2 = create_challenge(data_for_challenge, self.user2)
        challenge2.is_active = False
        challenge2.save()

        response = self.client.get(self.url)
        expected_data = [{
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'members_amount': 2,
            'bet': self.challenge.bet,
            'bets_sum': 100,
            'finish_datetime': self.challenge.finish_datetime
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)











