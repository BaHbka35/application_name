import os
import shutil

from django.urls import reverse
from django.test import override_settings
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status

from challenges.models import Challenge
from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, accept_challenge,\
                                         upload_video_for_challenge


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
    'description': 'you must make 20 pushups in 10 seconds',
    'requirements': 'stopwatch must be seen on video',
    'bet': 50
}


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class GetDetailChallengeTests(APITestCase):
    """
    Tests for testing getting detail
    information about specific challenge.
    """

    def setUp(self):
        """"""
        video_example_dir = 'video_examples/'
        self.__clear_video_example_test_directory(video_example_dir)

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

    def __clear_video_example_test_directory(self, dir: str) -> None:
        """Clear test directory that needs for stores video examples for challenge."""
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, dir))
        except:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, dir))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, dir))

    def test_get_detail_challenge_info_with_one_member(self):
        """Tests getting detail challenge information with one member."""
        response = self.client.get(self.url)
        expected_data = {
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'description': self.challenge.description,
            'requirements': self.challenge.requirements,
            'members_amount': 1,
            'bet': self.challenge.bet,
            'bets_sum': 50,
            'finish_datetime': str(self.challenge.finish_datetime),
            'video_example_path': self.video_example_path
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_challenge_info_with_two_member(self):
        """Tests getting detail challenge information with two members."""
        accept_challenge(self.user2, self.challenge)
        response = self.client.get(self.url)
        expected_data = {
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'description': self.challenge.description,
            'requirements': self.challenge.requirements,
            'members_amount': 2,
            'bet': self.challenge.bet,
            'bets_sum': 100,
            'finish_datetime': str(self.challenge.finish_datetime),
            'video_example_path': self.video_example_path
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_not_active_challenge_info(self):
        """Tests getting detail challenge info when challenge was finished."""
        accept_challenge(self.user2, self.challenge)
        self.challenge.is_active = False
        self.challenge.save()
        response = self.client.get(self.url)
        expected_data = {
            'challenge_id': self.challenge.id,
            'name': self.challenge.name,
            'creator': self.user.username,
            'goal': self.challenge.goal,
            'description': self.challenge.description,
            'requirements': self.challenge.requirements,
            'members_amount': 2,
            'bet': self.challenge.bet,
            'bets_sum': 100,
            'finish_datetime': str(self.challenge.finish_datetime),
            'video_example_path': self.video_example_path
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_detail_info_of_free_challenge(self):
        """Tests getting detail info about freee challenge."""
        data_for_challenge2 = data_for_challenge.copy()
        data_for_challenge2['name'] = 'other_name'
        data_for_challenge2['bet'] = 0
        challenge2 = create_challenge(data_for_challenge2, self.user)
        accept_challenge(self.user2, challenge2)

        kwargs = {'challenge_id': challenge2.id}
        url = reverse('challenges:get_detail_challenge', kwargs=kwargs)
        response = self.client.get(url)

        expected_data = {
            'challenge_id': challenge2.id,
            'name': challenge2.name,
            'creator': self.user.username,
            'goal': challenge2.goal,
            'description': challenge2.description,
            'requirements': challenge2.requirements,
            'members_amount': 2,
            'bet': challenge2.bet,
            'bets_sum': 0,
            'finish_datetime': challenge2.finish_datetime,
            'video_example_path': None
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)


    def test_get_detail_challenge_info_for_not_auth_user(self):
        """
        Tests getting detail challenge
        informatoion for not authenticted user.
        """
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_unexisting_challenge_info(self):
        """Tests getting information about challenge that doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:get_detail_challenge', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
























