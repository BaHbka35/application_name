import hashlib

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .models import User


class TokenService:
    """Class for different tokens."""

    @classmethod
    def get_activation_token(cls, user):
        """
        Create token which will be send on user email
        for activate user account.
        """
        forming_str = f"{user.id}{user.username}"
        forming_str = forming_str.encode()
        hash_object = hashlib.md5(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_activation_token(cls, token, user):
        """Check is givven token bolongs to current user"""
        return token == cls.get_activation_token(user)


class EmailService:
    """Class wich contain login for email sending."""

    @classmethod
    def send_email_for_activate_account(cls, request, user):
        """Send email to user email with activation link."""
        content = cls.__get_content_for_activation_email(request, user)
        ready_email = cls.__get_ready_activation_email(content, user)
        ready_email.send()

    def __get_content_for_activation_email(request, user):
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

    def __get_ready_activation_email(content, user):
        """Create email wich is ready to be sent to user."""
        subject = 'Account activation'
        html_message = render_to_string(
            'users/email_for_activation_account.html', content)
        user_email = user.email
        email = EmailMessage(subject, html_message, to=[user_email])
        return email


def create_user_and_send_email_for_activation(request, **data):
    user = User.objects.create_user(**data)
    EmailService.send_email_for_activate_account(request, user)
