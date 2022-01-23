from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from users.models import User
from .token_services import TokenService
from .datetime_services import DatetimeService


class EmailService:
    """Class witch contain logic for email sending."""

    @classmethod
    def send_email_for_activate_account(cls, request, user: User) -> None:
        """Send email to user email with activation link."""
        encrypted_datatime = DatetimeService.get_encrypted_datetime()
        token = TokenService.get_activation_token(user, encrypted_datatime)
        content = cls.__get_content_for_email(request, user, token,
                                              encrypted_datatime)
        ready_email = cls.__get_ready_activation_email(content, user)
        ready_email.send()

    @classmethod
    def __get_ready_activation_email(cls, content, user: User) -> EmailMessage:
        """Create activation email which is ready to be sent to user."""
        subject = 'Account activation'
        html_message = render_to_string(
            'users/email_for_activation_account.html', content)
        user_email = user.email
        email = EmailMessage(subject, html_message, to=[user_email])
        return email


    @classmethod
    def send_email_for_confirm_changing_email(
            cls, request, user: User, new_user_email: str) -> None:
        """
        Send email to new user email address
        for further confirmation his email
        """
        token = TokenService.get_email_confirmation_token(user, new_user_email)
        content = cls.__get_content_for_email(request, user, token)

        ready_email = cls.__get_ready_email_for_confirm_changing(
            content, new_user_email)

        ready_email.send()

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

    @classmethod
    def __get_content_for_email(cls, request, user: User, token: str,
                                encrypted_datatime: str) -> tuple:
        """Forms content for email latter."""
        current_site = get_current_site(request)
        content = {
            'user': user,
            'id': user.id,
            'encrypted_datatime': encrypted_datatime,
            'token': token,
            'domain': current_site.domain
        }
        return content
