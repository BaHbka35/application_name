import datetime
import base64

from cryptography.fernet import Fernet
from cryptography import fernet

from django.conf import settings


class DatetimeEncryptionService:
    """
    Class for encrypting datatime to string and
    decrypting string(encrypted datetime) to datetime
    """

    KEY_FOR_ENCRYPTION = base64.urlsafe_b64encode(
        settings.SECRET_KEY[:32].encode())

    fernet = Fernet(KEY_FOR_ENCRYPTION)

    datetime_format = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def get_encrypted_datetime(cls) -> str:
        """Return encrypted datetime in str representation."""
        datetime_obj_now = datetime.datetime.now()
        datetime_str_now = datetime_obj_now.strftime(cls.datetime_format)

        forming_str = datetime_str_now.encode()
        encrypted_datetime = cls.fernet.encrypt(forming_str)

        return encrypted_datetime.decode()

    @classmethod
    def get_decrypted_datetime(cls, encrypted_datetime: str) -> datetime:
        """Checks encrypted datetime. Return True if all is good."""
        encrypted_datetime_in_bytes = encrypted_datetime.encode()
        try:
            decrypted_datetime_in_bytes = cls.fernet.decrypt(
                encrypted_datetime_in_bytes)
        except fernet.InvalidToken:
            return False
        decrypted_datetime_str = decrypted_datetime_in_bytes.decode()
        datetime_obj = datetime.datetime.strptime(decrypted_datetime_str,
                                                  cls.datetime_format)
        return datetime_obj







