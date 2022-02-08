import os
import shutil

from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers
from challenges.services.challenge_services import ChallengeService


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
data_for_challenge = {
    'name': 'challenge_name',
    'finish_datetime': '2023-02-02 18:25:43',
    'goal': 'make 20 pushups in 10 seconds',
    'description': 'you mush make 20 pushups in 10 seconds',
    'requirements': 'stopwatch must be seen on video',
    'bet': 50
}

@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class UploadVideoExampleTests(APITestCase):
    """Class for tests upload video example for challenge."""


    def setUp(self):
        """Registrate, activate user."""
        video_example_dir = 'video_examples/'
        self.__clear_video_example_test_directory(video_example_dir)
        user = registrate_and_activate_user(signup_data)
        challenge = ChallengeService.create_challenge(data_for_challenge, user)

        kwargs = {'challenge_id': challenge.id}
        self.url = reverse('challenges:upload_video_example', kwargs=kwargs)

        file_path = os.path.join(settings.MEDIA_ROOT, 'video_source/111.mp4')
        video_for_test = SimpleUploadedFile(file_path, b'video')
        self.data = {'video_example': video_for_test}

        self.storage_dirrectory = os.path.join(settings.MEDIA_ROOT, video_example_dir)

        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

    def __clear_video_example_test_directory(self, dir: str) -> None:
        """Clear test directory that needs for stores video examples for challenge."""
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, dir))
        except:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, dir))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, dir))

    def test_upload_video_correct(self):
        """Tests uploading video when all is good."""
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(amount_files_in_dir), 1)

    def test_upload_video_of_user_that_not_auth(self):
        """Tests upload video example of user that not auth."""
        self.client.credentials()
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(amount_files_in_dir), 0)

    def test_upload_video_when_challenge_already_has_video_example(self):
        """Tests uploading video when challenge already has video example."""
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        response2 = self.client.put(self.url, data=self.data,
                                    format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(amount_files_in_dir), 1)

    def test_send_empty_json(self):
        """Tests sending empty json file."""
        data = {}
        response = self.client.put(self.url, data=data, format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(amount_files_in_dir), 0)

    def test_send_json_without_video_file(self):
        """Tests sending json without video file."""
        data = {'video_example': ''}
        response = self.client.put(self.url, data=data, format='multipart')
        amount_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(amount_files_in_dir), 0)








