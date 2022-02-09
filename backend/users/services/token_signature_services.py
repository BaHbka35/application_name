import hashlib

from django.conf import settings


class TokenSignatureService:
    """Class which contain logic linked with signatures for tokens."""

    @staticmethod
    def get_signature(token: str) -> str:
        """Return signature for given token."""
        forming_str = token.encode()
        hash_object = hashlib.sha256(forming_str + settings.SECRET_KEY_BYTES)
        return hash_object.hexdigest()

    @classmethod
    def check_signature(cls, token: str, given_signature: str) -> bool:
        """Checks that given signature is correct."""
        return cls.get_signature(token) == given_signature
