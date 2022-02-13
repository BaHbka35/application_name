import os

from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

from rest_framework.test import APITestCase
from rest_framework import status

from challenges.models import Challenge, ChallengeMember, ChallengeAnswer

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, clear_directory,\
                                         accept_challenge
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class AddAnswerOnChallenge(APITestCase):
    """Class for tests upload video example for challenge."""

    def __get_challenge_answer(self):
        challenge_member = ChallengeMember.objects.get(user=self.user2, challenge=self.challenge)
        challenge_answer = ChallengeAnswer.objects.get(challenge_member=challenge_member,
                                                       challenge=self.challenge)
        return challenge_answer

    def setUp(self):
        """"""
        self.video_answer_dir = os.path.join(settings.MEDIA_ROOT, 'video_answers/')
        clear_directory(self.video_answer_dir)

        user = registrate_and_activate_user(signup_data)
        self.challenge = create_challenge(data_for_challenge, user)

        self.file_name = '111.mp4'
        self.source_file_path = os.path.join(settings.MEDIA_ROOT, f'video_source/{self.file_name}')
        file = File(open(self.source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')
        self.video_answer_field_name = 'video_answer'
        self.data = {self.video_answer_field_name: uploaded_file}

        self.user2 = registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        kwargs = {'challenge_id': self.challenge.id}
        self.url = reverse('challenges:add_answer_on_challenge', kwargs=kwargs)

    def test_add_answer_on_challenge(self):
        """Tests adding answer on challenge."""
        accept_challenge(self.user2, self.challenge)
        response = self.client.put(self.url, data=self.data, format='multipart')

        challenge_answer = self.__get_challenge_answer()

        files_in_dir = os.listdir(self.video_answer_dir)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(files_in_dir), 1)
        self.assertEqual(challenge_answer.challenge, self.challenge)
        self.assertEqual(challenge_answer.challenge_member.user, self.user2)

    def test_add_answer_on_challenge_by_user_that_not_auth(self):
        """Tests adding answer on challenge by user that not auth."""
        accept_challenge(self.user2, self.challenge)
        self.client.credentials()
        response = self.client.put(self.url, data=self.data, format='multipart')
        files_in_dir = os.listdir(self.video_answer_dir)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(files_in_dir), 0)

    def test_add_answer_on_challenge_in_second_time(self):
        """Tests second adding answer on challenge by same user."""
        accept_challenge(self.user2, self.challenge)
        response = self.client.put(self.url, data=self.data, format='multipart')

        file = File(open(self.source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')
        data = {self.video_answer_field_name: uploaded_file}

        response2 = self.client.put(self.url, data=data, format='multipart')

        challenge_answer = self.__get_challenge_answer()
        files_in_dir = os.listdir(self.video_answer_dir)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(files_in_dir), 1)
        self.assertEqual(challenge_answer.challenge, self.challenge)
        self.assertEqual(challenge_answer.challenge_member.user, self.user2)

    def test_add_answer_for_not_existing_challenge(self):
        """Tests adding answer for challenge than doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:add_answer_on_challenge', kwargs=kwargs)
        response = self.client.put(url, data=self.data, format='multipart')

        files_in_dir = os.listdir(self.video_answer_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)

    def test_add_answer_on_challenge_by_not_member_of_challenge(self):
        """
        Tests adding answer for challenge by
        user that isn't a member of this challenge.
        """
        response = self.client.put(self.url, data=self.data, format='multipart')
        files_in_dir = os.listdir(self.video_answer_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)

    def test_add_answer_on_finished_challenge(self):
        """Tests adding answer on challenge that has already finished."""
        challenge = Challenge.objects.get()
        challenge.is_active = False
        challenge.save()
        response = self.client.put(self.url, data=self.data, format='multipart')
        files_in_dir = os.listdir(self.video_answer_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)









