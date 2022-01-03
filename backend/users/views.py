from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import SignUpSerializer
from .models import User
from .services import get_activation_token, send_email_for_activate_account


class SignUpView(APIView):
    """View for registration user"""

    def post(self, request):
        """
        Registrate user and return response
        about success registration or about fail
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email_for_activate_account(request, user)
            json = serializer.data
            json["message"] = "Check your email for activate account."
            return Response(data=json,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class AccountActivationView(APIView):
    """View for activate user account"""

    def get(self, request, id, token):
        print(id)
        print(token)
        user = User.objects.get(id=id)
        if token == get_activation_token(user):
            user.is_activated = True
            token = Token.objects.create(user=user)
            json = {
                "token": token.key,
                "message": "account was activated",
            }
            user.save()
            return Response(data=json, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
