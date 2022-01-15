import hashlib

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from rest_framework.authtoken.models import Token

from .models import User


class TokenService:
    """Class for different tokens."""

    @classmethod
    def get_activation_token(cls, user: User) -> str:
        """
        Create token which will be send on user email
        for activate user account.
        """
        forming_str = f"{user.id}{user.username}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_activation_token(cls, token: str, user: User) -> bool:
        """Check is givven token bolongs to current user"""
        return token == cls.get_activation_token(user)

    @classmethod
    def get_user_auth_token(cls, user: User) -> str:
        """Return user authentication token."""
        return Token.objects.get_or_create(user=user)[0].key

    @classmethod
    def delete_user_auth_token(cls, user: User) -> None:
        """Delete user authentication token."""
        token = Token.objects.get(user=user)
        token.delete()


class EmailService:
    """Class witch contain logic for email sending."""

    @classmethod
    def send_email_for_activate_account(cls, request, user: User) -> None:
        """Send email to user email with activation link."""
        content = cls.__get_content_for_activation_email(request, user)
        ready_email = cls.__get_ready_activation_email(content, user)
        ready_email.send()

    def __get_content_for_activation_email(request, user: User) -> dict:
        """
        Forms conten for latter which will be
        sent to user email fro activate account
        """
        token = TokenService.get_activation_token(user)
        current_site = get_current_site(request)
        content = {
            'user': user,
            'id': user.id,
            'token': token,
            'domain': current_site.domain
        }
        return content

    def __get_ready_activation_email(content, user: User) -> EmailMessage:
        """Create email wich is ready to be sent to user."""
        subject = 'Account activation'
        html_message = render_to_string(
            'users/email_for_activation_account.html', content)
        user_email = user.email
        email = EmailMessage(subject, html_message, to=[user_email])
        return email


class UserService:
    """Class witch contain all logic belongs to user"""

    @staticmethod
    def create_user_and_send_email_for_activation(request,
                                                  **data: dict) -> None:
        """
        Creates user and send him email with
        contain link for account activation
        """
        user = User.objects.create_user(**data)
        EmailService.send_email_for_activate_account(request, user)

    @staticmethod
    def activate_user(user: User) -> None:
        """Activates user account"""
        user.is_activated = True
        user.save()

    @staticmethod
    def change_user_password(user: User, password: str) -> None:
        """Changes user password"""
        user.set_password(password)
        user.save()

    @staticmethod
    def update_user_data(user: User, data: dict) -> None:
        """Update user data."""
        user.first_name = data['first_name']
        user.surname = data['surname']
        user.username = data['username']
        user.slug = user.username
        user.age = data['age']
        user.gender = data['gender']
        user.training_experience = data['training_experience']
        user.trains_now = data['trains_now']
        user.save()

