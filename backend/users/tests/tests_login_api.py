from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from users.services import TokenService


class LogInTests(APITestCase):

    url = reverse('users:login')

    def setUp(self):
        signup_data = {
            "first_name": "Sasha",
            "surname": "Kurkin",
            "username": "Luk",
            "email": "nepetr86@bk.ru",
            "password": "123456789",
            "password2": "123456789"
            }
        url = reverse('users:signup')
        self.client.post(url, signup_data, format='json')

        user = User.objects.get()
        activation_token = TokenService.get_activation_token(user)
        url = reverse('users:activate_account',
                      kwargs={"id": user.id, "token": activation_token})
        response = self.client.get(url)

    def test_login(self):
        data = {
            "username": "Luk",
            "password": "123456789",
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='Luk')
        self.assertEqual(user.is_authenticated, True)
