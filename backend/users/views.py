from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import SignUpSerializer
from .models import User
from .services import TokenService, EmailService,\
                      create_user_and_send_email_for_activation


class SignUpView(APIView):
    """View for registration user"""

    def post(self, request):
        """
        Registrate user and return response
        about success registration or about fail
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            create_user_and_send_email_for_activation(
                request, **serializer.data)
            json = serializer.data
            json["message"] = "Check your email for activate account."
            del json['password']
            return Response(data=json,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class AccountActivationView(APIView):
    """View for activate user account"""

    def get(self, request, id, token):
        """Activate user and return token for authontication."""
        try:
            user = User.objects.get(id=id)
        except:
            json = {"message": "Activation account is faild."}
            return Response(data=json, status=status.HTTP_400_BAD_REQUEST)
        if TokenService.check_activation_token(token, user):
            user.is_activated = True
            user.save()
            token = Token.objects.create(user=user)
            json = {
                "token": token.key,
                "message": "account was activated",
            }
            return Response(data=json, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
