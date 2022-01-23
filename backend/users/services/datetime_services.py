import datetime
import base64

from cryptography.fernet import Fernet
from cryptography import fernet

from django.conf import settings


class DatetimeService:

    KEY_FOR_ENCRUPTION = base64.urlsafe_b64encode(
        settings.SECRET_KEY[:32].encode())

    fernet = Fernet(KEY_FOR_ENCRUPTION)

    @classmethod
    def get_encrypted_datetime(cls) -> str:
        """Return encrypted datetime in str representation."""
        datetime_obj_now = datetime.datetime.now()
        datetime_str_now = datetime_obj_now.strftime("%Y-%m-%d %H:%M:%S")

        forming_str = datetime_str_now.encode()
        encrypted_datetime = cls.fernet.encrypt(forming_str)

        return encrypted_datetime.decode()

    @classmethod
    def check_encrypted_datetime(cls, encrypted_datetime: str) -> bool:
        """Checks encrypted datetime. Return True if all is good."""
        encrypted_datetime_bytes = encrypted_datetime.encode()
        try:
            a = cls.fernet.decrypt(encrypted_datetime_bytes)
        except fernet.InvalidToken:
            return False
        datetime_str = a.decode()

        datetimeobj = datetime.datetime.strptime(datetime_str,
                                                 "%Y-%m-%d %H:%M:%S")
        datatime_now = datetime.datetime.now()
        time_difference = datatime_now - datetimeobj

        return not time_difference.total_seconds() > 9438535
