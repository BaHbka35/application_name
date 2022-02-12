import os

from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, clear_directory
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class AddAnswerOnChallenge(APITestCase):
    """Class for tests upload video example for challenge."""

    def setUp(self):
        """"""
        video_answer_dir = os.path.join(settings.MEDIA_ROOT, 'video_answer/')
        clear_directory(video_answer_dir)

        user = registrate_and_activate_user(signup_data)
        challenge = create_challenge(data_for_challenge, user)

        file_path = os.path.join(settings.MEDIA_ROOT, 'video_source/111.mp4')
        file = File(open(file_path, 'rb'))
        uploaded_file = SimpleUploadedFile('111.mp4', file.read(),
                                           content_type='multipart/form-data')

        self.data = {'video_example': uploaded_file}

        self.storage_dirrectory = os.path.join(settings.MEDIA_ROOT, video_answer_dir)

        self.user2 = registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        kwargs = {'challenge_id': challenge.id}
        self.url = reverse('challenges:upload_video_example', kwargs=kwargs)

    def test_add_answer_on_challenge(self):
        """Tests adding asnwer on challenge."""
        response = self.client.put(self.url, data=self.data, format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(amount_files_in_dir), 1)

    def test_add_answer_on_challenge_by_user_that_not_auth(self):
        """Tests adding answer on challenge by user that not auth."""
        self.client.credentials()
        response = self.client.put(self.url, data=self.data, format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(amount_files_in_dir), 0)

    def test_add_answer_on_challenge_in_second_time(self):
        """Tests second adding answer on challenge by same user."""
        response = self.client.put(self.url, data=self.data, format='multipart')

        file_path = os.path.join(settings.MEDIA_ROOT, 'video_source/111.mp4')
        file = File(open(file_path, 'rb'))
        uploaded_file = SimpleUploadedFile('111.mp4', file.read(),
                                           content_type='multipart/form-data')
        data = {'video_example': uploaded_file}

        response2 = self.client.put(self.url, data=data, format='multipart')

        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code2, status.HTTP_200_OK)
        self.assertEqual(len(amount_files_in_dir), 1)

    def test_add_answer_for_not_existing_challenge(self):
        """Tests adding asnswer for challenge than doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:get_challenge_members', kwargs=kwargs)
        response = self.client.put(self.url, data=self.data, format='multipart')

        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(amount_files_in_dir), 0)










