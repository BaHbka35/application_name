import os
from typing import Optional

from django.urls import reverse
from django.test import override_settings
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from challenges.models import Challenge
from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, accept_challenge,\
                                         upload_video_for_challenge, clear_directory
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


def get_expected_data(challenge: Challenge, user: User, file_path: Optional[str] = None) -> dict:
    expected_data = {
        'challenge_id': challenge.id,
        'name': challenge.name,
        'creator': user.username,
        'goal': challenge.goal,
        'description': challenge.description,
        'requirements': challenge.requirements,
        'members_amount': None,
        'bet': challenge.bet,
        'bets_sum': None,
        'finish_datetime': str(challenge.finish_datetime),
        'video_example_path': file_path
    }
    return expected_data


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class GetDetailChallengeTests(APITestCase):
    """
    Tests for testing getting detail
    information about specific challenge.
    """

    def setUp(self):
        """"""
        video_example_dir = os.path.join(settings.MEDIA_ROOT, 'video_examples/')
        clear_directory(video_example_dir)

        self.user = registrate_and_activate_user(signup_data)
        self.challenge = create_challenge(data_for_challenge, self.user)

        upload_video_for_challenge(self.user, self.challenge, settings.MEDIA_ROOT)
        self.challenge = Challenge.objects.get(id=self.challenge.id)
        self.video_example_path = self.challenge.video_example.path

        self.user2 = registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        kwargs = {'challenge_id': self.challenge.id}
        self.url = reverse('challenges:get_detail_challenge', kwargs=kwargs)

    def test_get_detail_challenge_info_with_one_member(self):
        """Tests getting detail challenge information with one member."""
        response = self.client.get(self.url)
        expected_data = get_expected_data(self.challenge, self.user, self.video_example_path)
        expected_data['members_amount'] = 1
        expected_data['bets_sum'] = 50
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_challenge_info_with_two_member(self):
        """Tests getting detail challenge information with two members."""
        accept_challenge(self.user2, self.challenge)
        response = self.client.get(self.url)
        expected_data = get_expected_data(self.challenge, self.user, self.video_example_path)
        expected_data['members_amount'] = 2
        expected_data['bets_sum'] = 100
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_not_active_challenge_info(self):
        """Tests getting detail challenge info when challenge was finished."""
        accept_challenge(self.user2, self.challenge)
        self.challenge.is_active = False
        self.challenge.save()
        response = self.client.get(self.url)
        expected_data = get_expected_data(self.challenge, self.user, self.video_example_path)
        expected_data['members_amount'] = 2
        expected_data['bets_sum'] = 100
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_info_of_free_challenge(self):
        """Tests getting detail info about free challenge."""
        data_for_challenge2 = data_for_challenge.copy()
        data_for_challenge2['name'] = 'other_name'
        data_for_challenge2['bet'] = 0
        challenge2 = create_challenge(data_for_challenge2, self.user)
        accept_challenge(self.user2, challenge2)

        kwargs = {'challenge_id': challenge2.id}
        url = reverse('challenges:get_detail_challenge', kwargs=kwargs)
        response = self.client.get(url)

        expected_data = get_expected_data(challenge2, self.user)
        expected_data['members_amount'] = 2
        expected_data['bets_sum'] = 0
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_challenge_info_for_not_auth_user(self):
        """
        Tests getting detail challenge
        information for not authenticated user.
        """
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_challenge_info_that_doesnt_exist(self):
        """Tests getting information about challenge that doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:get_detail_challenge', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
























