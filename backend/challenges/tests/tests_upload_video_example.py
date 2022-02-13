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
class UploadVideoExampleTests(APITestCase):
    """Class for tests upload video example for challenge."""

    def setUp(self):
        """Registrate, activate user."""
        self.video_example_dir = os.path.join(settings.MEDIA_ROOT, 'video_examples/')
        clear_directory(self.video_example_dir)

        user = registrate_and_activate_user(signup_data)
        challenge = create_challenge(data_for_challenge, user)

        source_file_name = '111.mp4'
        source_file_path = os.path.join(settings.MEDIA_ROOT, f'video_source/{source_file_name}')

        source_file = File(open(source_file_path, 'rb'))
        uploaded_file = SimpleUploadedFile(source_file_name, source_file.read(),
                                           content_type='multipart/form-data')
        self.video_example_field_name = 'video_example'
        self.data = {self.video_example_field_name: uploaded_file}

        auth_headers = get_auth_headers(login_data)
        set_auth_headers(self, auth_headers)

        kwargs = {'challenge_id': challenge.id}
        self.url = reverse('challenges:upload_video_example', kwargs=kwargs)

    def test_upload_video_correct(self):
        """Tests uploading video when all is good."""
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(files_in_dir), 1)

    def test_upload_video_of_user_that_not_auth(self):
        """Tests upload video example of user that not auth."""
        self.client.credentials()
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(files_in_dir), 0)

    def test_upload_video_when_challenge_already_has_video_example(self):
        """Tests uploading video when challenge already has video example."""
        response = self.client.put(self.url, data=self.data,
                                   format='multipart')

        file_path = os.path.join(settings.MEDIA_ROOT, 'video_source/111.mp4')
        file = File(open(file_path, 'rb'))
        uploaded_file = SimpleUploadedFile('111.mp4', file.read(),
                                           content_type='multipart/form-data')
        data = {self.video_example_field_name: uploaded_file}
        response2 = self.client.put(self.url, data=data,
                                    format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(files_in_dir), 1)

    def test_send_empty_json(self):
        """Tests sending empty json file."""
        data = {}
        response = self.client.put(self.url, data=data, format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)

    def test_send_json_without_video_file(self):
        """Tests sending json without video file."""
        data = {self.video_example_field_name: ''}
        response = self.client.put(self.url, data=data, format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)

    def test_upload_video_example_by_user_who_is_not_a_creator(self):
        """
        Tests uploading video example by user
        that isn't a challenge creator.
        """
        registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        response = self.client.put(self.url, data=self.data,
                                   format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)

    def test_upload_video_example_for_challenge_that_does_not_exist(self):
        """Tests uploading video example with challenge_id that doesn't exist."""
        kwargs = {'challenge_id': 348}
        url = reverse('challenges:upload_video_example', kwargs=kwargs)
        response = self.client.put(url, data=self.data, format='multipart')
        files_in_dir = os.listdir(self.video_example_dir)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(files_in_dir), 0)



