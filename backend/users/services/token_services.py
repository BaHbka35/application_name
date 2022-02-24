import hashlib
import datetime

from typing import Optional

from django.conf import settings

from rest_framework.authtoken.models import Token

from users.models import User

from .datetime_services import DatetimeEncryptionService


class ActivationTokenService:

    @classmethod
    def get_activation_token(cls, user: User, encrypted_datetime: str) -> str:
        """
        Create token which will be sent on user email
        for activate user account.
        """
        forming_str = f"{user.id}{user.username}{encrypted_datetime}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def is_activation_token_valid(cls, user: User, encrypted_datetime: str,
                                  token: str) -> tuple[bool, Optional[dict]]:
        """Checks activation token. If all is good return True."""
        decrypted_datetime = DatetimeEncryptionService.get_decrypted_datetime(
            encrypted_datetime)
        if not cls.is_activation_token_belonged_to_current_user(
                user, encrypted_datetime, token):
            data = {'message': 'Token isn\'t valid.'}
            return False, data
        if not TokenService.check_token_lifetime(decrypted_datetime):
            data = {'message': 'Lifetime of token is finished.'}
            return False, data
        return True, None

    @classmethod
    def is_activation_token_belonged_to_current_user(
            cls, user: User, encrypted_datetime: str, token: str) -> bool:
        """Check is given token belongs to current user."""
        return token == cls.get_activation_token(user, encrypted_datetime)


class AuthenticationTokenService:

    @classmethod
    def get_user_authentication_token(cls, user: User) -> str:
        """Return user authentication token."""
        return Token.objects.get_or_create(user=user)[0].key

    @classmethod
    def delete_user_authentication_token(cls, user: User) -> None:
        """Delete user authentication token."""
        Token.objects.get(user=user).delete()


class EmailConfirmationTokenService:

    @classmethod
    def get_email_confirmation_token(cls, user: User, encrypted_datetime: str,
                                     new_user_email: str) -> str:
        """
        Create token which will be sent on new
        user email for confirm changing email.
        """
        forming_str = f"{user.id}{new_user_email}{encrypted_datetime}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def is_email_confirmation_token_valid(
            cls, user: User, encrypted_datetime: str, token: str,
            new_user_email: str) -> tuple[bool, Optional[dict]]:
        """Checks activation token. If all is good return True."""
        decrypted_datetime = DatetimeEncryptionService.get_decrypted_datetime(
            encrypted_datetime)
        if not cls.is_email_confirmation_token_belongs_to_current_user(
                user, encrypted_datetime, token, new_user_email):
            data = {'message': 'Email confirmation token isn\'t valid.'}
            return False, data
        if not TokenService.check_token_lifetime(decrypted_datetime):
            data = {'message': 'Lifetime of email confiramtion token is finished.'}
            return False, data
        return True, None

    @classmethod
    def is_email_confirmation_token_belongs_to_current_user(
            cls, user: User, encrypted_datetime: str, token: str, new_user_email: str
    ) -> bool:
        """Check is given token belongs to user who is changing email."""
        return token == cls.get_email_confirmation_token(
            user, encrypted_datetime, new_user_email)


class TokenService:
    """Class for different tokens."""

    @classmethod
    def check_token_lifetime(cls, datetime_obj: datetime) -> bool:
        """Checks is token lifetime is available."""
        datetime_now = datetime.datetime.now()
        time_difference = datetime_now - datetime_obj
        return not time_difference.total_seconds() > 60 * 60 * 24









