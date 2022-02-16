import os

from typing import Optional

from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

from challenges.models import Challenge, ChallengeMember, ChallengeAnswer

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, clear_directory,\
                                         accept_challenge, add_answer_on_challenge
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


def get_expected_data(user: User, video_link: Optional[str] = None) -> dict:
    expected_data = {
        'challenge_member': user.username,
        'video_answer_path': video_link
    }
    return expected_data


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test/')
class GetChallengeAnswersTests(APITestCase):
    """Class for tests getting answers which belongs to specific challenge."""

    def setUp(self):
        """"""
        self.video_answer_dir = os.path.join(settings.MEDIA_ROOT, settings.CHALLENGE_ANSWERS_DIR)
        clear_directory(self.video_answer_dir)

        self.user = registrate_and_activate_user(signup_data)
        self.challenge = create_challenge(data_for_challenge, self.user)
        self.challenge_member = ChallengeMember.objects.get(
            user=self.user, challenge=self.challenge)

        self.file_name = '111.mp4'
        self.source_file_path = os.path.join(settings.MEDIA_ROOT,
                                             f'video_source/{self.file_name}')
        file = File(open(self.source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')

        challenge_answer = add_answer_on_challenge(self.challenge_member,
                                                   self.challenge, uploaded_file)

        self.user2 = registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        accept_challenge(self.user2, self.challenge)

        self.challenge_member2 = ChallengeMember.objects.get(
            user=self.user2, challenge=self.challenge)

        file = File(open(self.source_file_path, 'rb'))
        uploaded_file2 = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')
        challenge_answer2 = add_answer_on_challenge(self.challenge_member2,
                                                    self.challenge, uploaded_file2)

        kwargs = {'challenge_id': self.challenge.id}
        self.url = reverse('challenges:get_challenge_answers', kwargs=kwargs)

        self.video_example_path = settings.MEDIA_URL + challenge_answer.video_answer.name
        self.video_example_path2 = settings.MEDIA_URL + challenge_answer2.video_answer.name

    def test_get_challenge_answers_when_challenge_is_active(self):
        """Tests getting challenge asnwers when challenge is active"""
        response = self.client.get(self.url)
        expected_data = get_expected_data(self.user2, self.video_example_path2)
        expected_data = [expected_data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_challenge_answers_when_challenge_is_finished(self):
        """Tests getting challenge_answers when challenge is finished"""
        self.challenge.is_active = False
        self.challenge.save()

        response = self.client.get(self.url)
        expected_data1 = get_expected_data(self.user, self.video_example_path)
        expected_data2 = get_expected_data(self.user2, self.video_example_path2)
        expected_data = [expected_data1, expected_data2]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_challenge_answers_for_not_auth_user(self):
        """Tests getting challenge_answers for not authenticated user."""
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_challenge_answers_of_unexisting_challenge(self):
        """Tests getting answer of challenge that doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:get_detail_challenge', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_challenge_answers_for_user_that_not_member(self):
        """
        Tests getting challenge answers for user
        that isn't a member of specific challenge.
        """
        data_for_challenge_local = data_for_challenge.copy()
        data_for_challenge_local['name'] = 'some_name'
        challenge2 = create_challenge(data_for_challenge_local, self.user)

        file = File(open(self.source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')

        challenge_member = ChallengeMember.objects.get(
            user=self.user, challenge=challenge2)
        challenge_answer = add_answer_on_challenge(challenge_member,
                                                   challenge2, uploaded_file)

        kwargs = {'challenge_id': challenge2.id}
        url = reverse('challenges:get_challenge_answers', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_challenge_answer_if_user_did_not_make_answer(self):
        """
        Tests getting challenge answer for user
        that hasn't made answer on this challenge.
        """
        data_for_challenge_local = data_for_challenge.copy()
        data_for_challenge_local['name'] = 'some_name'
        challenge2 = create_challenge(data_for_challenge_local, self.user)

        file = File(open(self.source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(self.file_name, file.read(),
                                           content_type='multipart/form-data')

        challenge_member = ChallengeMember.objects.get(
            user=self.user, challenge=challenge2)
        challenge_answer = add_answer_on_challenge(challenge_member,
                                                   challenge2, uploaded_file)

        accept_challenge(self.user2, challenge2)

        kwargs = {'challenge_id': challenge2.id}
        url = reverse('challenges:get_challenge_answers', kwargs=kwargs)
        response = self.client.get(url)

        expected_data = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_challenge_answer_when_challenge_is_finished_without_answers(self):
        """
        Tests getting challenge answer for challenge
        that was finished and that doesn't have answers.
        """
        data_for_challenge_local = data_for_challenge.copy()
        data_for_challenge_local['name'] = 'some_name'
        challenge2 = create_challenge(data_for_challenge_local, self.user)
        challenge2.is_active = False
        challenge2.save()

        accept_challenge(self.user2, challenge2)

        kwargs = {'challenge_id': challenge2.id}
        url = reverse('challenges:get_challenge_answers', kwargs=kwargs)
        response = self.client.get(url)

        expected_data = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)









