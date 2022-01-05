import json

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import SignUpSerializer, LogInSerializer,\
                         UsersListSerializer, ChangePasswordSerializer
from .models import User
from .services import TokenService, create_user_and_send_email_for_activation


class SignUpView(APIView):
    """View for registration user"""

    def post(self, request):
        """
        Registrate user and send email for account activation.
        Return response about success registration or about fail
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
        """
        Activate user and return response
        about success registration or about fail.
        """
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
    """
    View for authenticate user and return him token
    for further authentication and authorization.
    """

    def post(self, request):
        """
        Authenticate user and return response with data
        with contain private token for authentication
        """
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = self.__get_authenticated_user(serializer.data)
            if not user:
                data={"message": "Username or password uncorrect."}
                return Response(data=data,
                                status=status.HTTP_400_BAD_REQUEST)
            if user.is_activated:

                data_with_user_auth_token = self.__add_user_auth_token_in_data(
                    user, serializer.data)
                return Response(data=data_with_user_auth_token,
                                status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def __get_authenticated_user(self, data):
        """Authenticate user and return him."""
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        return user

    def __add_user_auth_token_in_data(self, user, data):
        """
        Adds user authentication token in data witch was given.
        """
        token = Token.objects.get_or_create(user=user)[0].key
        data["token"] = token
        return data


class UsersListView(APIView):
    """View for getting users list."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns list of users."""
        users_list = json.loads(json.dumps(self.__get_users_list()))
        return Response(data=users_list, status=status.HTTP_200_OK)

    def __get_users_list(self):
        """Create queryset than serialize it and return users list."""
        queryset = User.objects.all()
        serializer = UsersListSerializer(queryset, many=True)
        return serializer.data


class LogOutView(APIView):
    """View for logs user out."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Logs user out."""
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response(status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """View for change user password."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change user password and delete his authentication token."""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data["new_password"])
            user.save()
            token = Token.objects.get(user=user)
            token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
