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
        Create token which will be sent on user email
        for activate user account.
        """
        forming_str = f"{user.id}{user.username}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_activation_token(cls, token: str, user: User) -> bool:
        """Check is given token belongs to current user."""
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

    @classmethod
    def get_email_confirmation_token(cls, user: User,
                                     new_user_email: str) -> str:
        """
        Create token which will be sent on new user email for confirm changing email.
        """
        forming_str = f"{user.id}{user.username}{new_user_email}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_email_confirmation_token(cls, token: str, user: User,
                                       new_user_email: str) -> bool:
        """Check is given token belongs to user who is changing email."""
        return token == cls.get_email_confirmation_token(user, new_user_email)


class EmailService:
    """Class witch contain logic for email sending."""

    @classmethod
    def send_email_for_activate_account(cls, request, user: User) -> None:
        """Send email to user email with activation link."""
        content = cls.__get_content_for_activation_email(request, user)
        ready_email = cls.__get_ready_activation_email(content, user)
        ready_email.send()

    @classmethod
    def __get_content_for_activation_email(cls, request, user: User) -> dict:
        """
        Forms content for latter which will be
        sent to user email for activate account.
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

    @classmethod
    def __get_ready_activation_email(cls, content, user: User) -> EmailMessage:
        """Create email witch is ready to be sent to user."""
        subject = 'Account activation'
        html_message = render_to_string(
            'users/email_for_activation_account.html', content)
        user_email = user.email
        email = EmailMessage(subject, html_message, to=[user_email])
        return email


    @classmethod
    def send_email_for_confirm_changing_email(
            cls, request, user: User, new_user_email: str) -> None:
        """Send email to new user email address for further confirmation his email"""
        content = cls.__get_content_for_confirm_changing_email(
                    request, user, new_user_email)
        ready_email = cls.__get_ready_email_for_confirm_changing(
                        content, new_user_email)
        ready_email.send()

    @classmethod
    def __get_content_for_confirm_changing_email(
            cls, request, user: User, new_user_email: str) -> dict:
        """
        Forms content for latter which will be sent to
        new user email for new email confirmation.
        """
        token = TokenService.get_email_confirmation_token(user, new_user_email)
        current_site = get_current_site(request)
        content = {
            'user': user,
            'id': user.id,
            'token': token,
            'domain': current_site.domain
        }
        return content

    @classmethod
    def __get_ready_email_for_confirm_changing(
            cls, content, new_user_email: str) -> EmailMessage:
        """Create email witch is ready to be sent to new user email."""
        subject = 'Email confirmation'
        html_message = render_to_string(
            'users/email_for_email_confirmation.html', content)
        user_email = new_user_email
        email = EmailMessage(subject, html_message, to=[user_email])
        return email


class UserService:
    """Class witch contain all logic belongs to user"""

    @staticmethod
    def create_user_and_send_email_for_activation(request,
                                                  **data: dict) -> User:
        """
        Creates user and send him email with
        link for activation his account.
        """
        user = User.objects.create_user(**data)
        EmailService.send_email_for_activate_account(request, user)
        return user

    @staticmethod
    def activate_user(user: User) -> User:
        """Activates user account."""
        user.is_activated = True
        user.save()
        return user

    @staticmethod
    def change_user_password(user: User, password: str) -> User:
        """Changes user password."""
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_user_data(user: User, data: dict) -> User:
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
        return user