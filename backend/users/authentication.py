from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token

from .services.token_signature_services import TokenSignatureService


class TokenAndSignatureAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request) -> tuple:
        """
        Custom user authentication. For authenticate
        user, is needed token and signature
        """
        token = request.META.get('HTTP_TOKEN')
        signature = request.META.get('HTTP_SIGNATURE')
        if not token or not signature:
            return None

        if not TokenSignatureService.check_signature(token, signature):
            return None

        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFaild('No such token')
        user = token_obj.user

        return user, token
