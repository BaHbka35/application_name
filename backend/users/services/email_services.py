from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from users.models import User, NotConfirmedEmail
from .token_services import ActivationTokenService, EmailConfirmationTokenService
from .datetime_services import DatetimeEncryptionService


class EmailSendingService:
    """Class which contain logic that is connected with email sending."""

    @classmethod
    def send_email_for_activate_account(cls, current_site_domain, user: User) -> None:
        """Send email to user email with activation link."""
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        token = ActivationTokenService.get_activation_token(user, encrypted_datetime)
        content = cls.__get_content_for_email(current_site_domain, user, token,
                                              encrypted_datetime)
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
            cls, current_site_domain, user: User, new_user_email: str) -> None:
        """
        Send email to new user email address
        for further confirmation his email
        """
        encrypted_datetime = DatetimeEncryptionService.get_encrypted_datetime()
        token = EmailConfirmationTokenService.get_email_confirmation_token(
            user, encrypted_datetime, new_user_email)
        content = cls.__get_content_for_email(current_site_domain, user,
                                              token, encrypted_datetime)
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
    def __get_content_for_email(cls, current_site_domain, user: User, token: str,
                                encrypted_datetime: str) -> tuple:
        """Forms content for email latter."""
        content = {
            'user': user,
            'id': user.id,
            'encrypted_datetime': encrypted_datetime,
            'token': token,
            'domain': current_site_domain
        }
        return content


class EmailAddressHandlingService:
    """Service for different actions with email addresses."""

    @staticmethod
    def add_email_address_to_not_confirmed(user: User, new_user_email: str) -> None:
        """Add email to not confirmed emails list"""
        try:
            not_confirmed_email = NotConfirmedEmail.objects.get(user=user)
        except NotConfirmedEmail.DoesNotExist:
            not_confirmed_email = None

        if not_confirmed_email:
            not_confirmed_email.delete()
        NotConfirmedEmail(user=user, email=new_user_email).save()
















