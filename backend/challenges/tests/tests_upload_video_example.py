import os
import shutil

from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from challenges.models import Challenge
from services_for_tests.for_tests import registrate_user, activate_user, \
                                         login_user, get_auth_headers, \
                                         set_auth_headers
from challenges.services.challenge_services import ChallengeService


signup_data = {
    'first_name': 'Sasha',
    'surname': 'Kurkin',
    'username': 'Luk',
    'email': 'nepetr86@bk.ru',
    'password': '123456789',
    'password2': '123456789'
}

login_data = {
    'username': 'Luk',
    'password': '123456789'
}


@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'test'),
                   MEDIA_URL='/media/test')
class UploadVideoExampleTests(APITestCase):
    """Class for tests upload video example for challenge."""



    def setUp(self):
        """Registrate, activate user."""
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'video_examples/'))
        except:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'video_examples/'))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'video_examples/'))

        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)

        data_for_challenge = {
            'name': 'challenge_name',
            'finish_datetime': '2023-02-02 18:25:43',
            'goal': 'make 20 pushups in 10 seconds',
            'description': 'you mush make 20 pushups in 10 seconds',
            'requirements': 'stopwatch must be seen on video',
            'bet': 50
        }
        user = User.objects.get()
        challenge = ChallengeService.create_challenge(data_for_challenge, user)
        kwargs = {'challenge_id': challenge.id}
        self.url = reverse('challenges:upload_video_example', kwargs=kwargs)

        file_path = os.path.join(settings.MEDIA_ROOT, 'video_source/111.mp4')
        self.storage_dirrectory = os.path.join(settings.MEDIA_ROOT,
                                               'video_examples/')
        video_for_test = SimpleUploadedFile(file_path, b'video')

        self.data = {'video_example': video_for_test,}

    def test_upload_video_correct(self):
        """Tests uploading video when all is good."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        amout_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(amout_files_in_dir), 1)

    def test_upload_video_when_challenge_already_has_video_example(self):
        """Tests uploading vidoe when challenge already has vidoe example."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        response2 = self.client.put(self.url, data=self.data,
                                   format='multipart')
        amout_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(amout_files_in_dir), 1)

    def test_send_ematy_json(self):
        """Tests sedning empty json file."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        data = {}
        response = self.client.put(self.url, data=data, format='multipart')
        amout_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(amout_files_in_dir), 0)

    def test_send_json_without_video_file(self):
        """Tests sending json without video file."""
        token, signature = get_auth_headers(self, login_data)
        set_auth_headers(self, token, signature)
        data = {'video_example': '',}
        response = self.client.put(self.url, data=data, format='multipart')
        amout_files_in_dir = os.listdir(self.storage_dirrectory)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(amout_files_in_dir), 0)
























