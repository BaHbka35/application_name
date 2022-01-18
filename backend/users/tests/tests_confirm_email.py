from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User, NotConfirmedEmail
from users.services import TokenService
from .for_tests import registrate_user, activate_user, login_user


signup_data = {
    "first_name": "Sasha",
    "surname": "Kurkin",
    "username": "Luk",
    "email": "nepetr86@bk.ru",
    "password": "123456789",
    "password2": "123456789"
    }

login_data = {
    "username": "Luk",
    "password": "123456789",
    }


class EmailConfirmationTests(APITestCase):


    def setUp(self):
        response = registrate_user(self, signup_data)
        user = User.objects.get(username=response.data['username'])
        activate_user(self, user)
        self.new_user_email = 'tochno_ne_danil@mail.ru'


        response = login_user(self, login_data)
        user_auth_token = response.data['token']


        changing_email_data = {
            'new_user_email': 'tochno_ne_danil@mail.ru'
        }
        changing_email_url = reverse('users:change_user_email')
        auth_header = 'Token ' + user_auth_token
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = self.client.put(changing_email_url, data=changing_email_data,
                                   format='json')



        token = TokenService.get_email_confirmation_token(user, self.new_user_email)
        kwargs = {
            'id': user.id,
            'token': token,
        }
        self.url = reverse('users:email_confirmation', kwargs=kwargs)

    def test_confirm_user_email(self):
        response = self.client.get(self.url)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.email, self.new_user_email)
        self.assertEqual(NotConfirmedEmail.objects.count(), 0)
