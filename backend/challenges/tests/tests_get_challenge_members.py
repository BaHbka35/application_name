from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from services_for_tests.for_tests import registrate_and_activate_user, \
                                         get_auth_headers, set_auth_headers,\
                                         create_challenge, accept_challenge
from services_for_tests.data_for_tests import signup_data, login_data, \
                                              signup_data2, login_data2, \
                                              data_for_challenge


class GetChallengeMembersTests(APITestCase):
    """Tests for testing getting members of specific challenge."""

    def setUp(self):
        """"""
        self.user = registrate_and_activate_user(signup_data)
        self.challenge = create_challenge(data_for_challenge, self.user)

        self.user2 = registrate_and_activate_user(signup_data2)
        auth_headers2 = get_auth_headers(login_data2)
        set_auth_headers(self, auth_headers2)

        kwargs = {'challenge_id': self.challenge.id}
        self.url = reverse('challenges:get_challenge_members', kwargs=kwargs)

    def test_get_challenge_member_with_one_person(self):
        """
        Tests getting list of challenge
        member that contain only one user.
        """
        response = self.client.get(self.url)
        expected_data = [
            {
                'user_id': self.user.id,
                'username': self.user.username
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_challenge_member_with_two_persons(self):
        """
        Tests getting list of challenge
        member that contain more than one person.
        """
        accept_challenge(self.user2, self.challenge)
        response = self.client.get(self.url)
        expected_data = [
            {
                'user_id': self.user.id,
                'username': self.user.username
            },
            {
                'user_id': self.user2.id,
                'username': self.user2.username
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data==expected_data, True)

    def test_get_challenge_members_by_not_auth_user(self):
        """Tests getting challenge members when user isn't authenticated."""
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_challenge_members_of_not_existing_challenge(self):
        """Tests getting members of challenge that doesn't exist."""
        kwargs = {'challenge_id': 100000000}
        url = reverse('challenges:get_challenge_members', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)














