from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import SignUpSerializer, LogInSerializer,\
                         UsersListSerializer
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
            data = {
                "message": "account was activated",
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            password = serializer.data["password"]
            user = authenticate(username=username, password=password)

            if not user:
                data={"message": "Username or password uncorrect."}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            token = Token.objects.get_or_create(user=user)[0].key
            data = serializer.data
            data["token"] = token
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UsersListSerializer(queryset, many=True)
        # if serializer.is_valid():
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
