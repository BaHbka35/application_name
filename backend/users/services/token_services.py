import hashlib

from django.conf import settings

from rest_framework.authtoken.models import Token

from users.models import User


class TokenService:
    """Class for different tokens."""

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
    def check_activation_token(cls, user: User, encrypted_datetime,
                               token: str) -> bool:
        """Check is given token belongs to current user."""
        return token == cls.get_activation_token(user, encrypted_datetime)

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
    def get_email_confirmation_token(cls, user: User, new_user_email: str,
                                     encrypted_datetime: str) -> str:
        """
        Create token which will be sent on new user email for confirm changing email.
        """
        forming_str = f"{user.id}{new_user_email}{encrypted_datetime}"
        forming_str = forming_str.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_email_confirmation_token(
            cls, user: User, encrypted_datetime: str, token: str, new_user_email: str
            ) -> bool:
        """Check is given token belongs to user who is changing email."""
        return token == cls.get_email_confirmation_token(user, encrypted_datetime, new_user_email)









