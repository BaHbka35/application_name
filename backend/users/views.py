from typing import Optional
import json

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import SignUpSerializer, LogInSerializer, \
                         UsersListSerializer, ChangePasswordSerializer, \
                         UpdateUserDateSerializer, ChangeUserEmailSerializer
from .models import User, NotConfirmedEmail
from .services.email_services import EmailService
from .services.token_services import TokenService
from .services.user_services import UserService
from .services.token_signature_services import TokenSignatureService


class SignUpView(APIView):
    """View for registration user."""

    def post(self, request) -> Response:
        """
        Registrate user and send email for account activation.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.create_user_and_send_email_for_activation(
            request, **serializer.data)
        data = serializer.data
        data["message"] = "Check your email for activate account."
        del data['password']
        return Response(data=data, status=status.HTTP_201_CREATED)


class AccountActivationView(APIView):
    """View for activate user account."""

    def get(self, request, id: int, token: str) -> Response:
        """Activate user."""
        try:
            user = User.objects.get(id=id)
        except:
            data = {"message": "Activation account is failed."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if TokenService.check_activation_token(token, user):
            UserService.activate_user(user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    """
    View for authenticate user and return him token
    for further authentication and authorization.
    """

    def post(self, request) -> Response:
        """
        Authenticate user and return response
        with token for further authentication.
        """
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = self.__get_authenticated_user(serializer.data)
            if not user:
                data = {"message": "Username or password incorrect."}
                return Response(data=data,
                                status=status.HTTP_400_BAD_REQUEST)
            if user.is_activated:
                token = TokenService.get_user_auth_token(user)
                signature = TokenSignatureService.get_signature(token)
                data = {'token': token, 'signature': signature}
                return Response(data=data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def __get_authenticated_user(self, data: dict) -> Optional[User]:
        """Authenticate user and return user or None."""
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        return user


class LogOutView(APIView):
    """View for logs user out."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Logs user out."""
        user = request.user
        TokenService.delete_user_auth_token(user)
        return Response(status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """View for change user password."""

    permission_classes = [IsAuthenticated]

    def put(self, request) -> Response:
        """Change user password and delete his authentication token."""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        UserService.change_user_password(
            user, serializer.data["new_password"])
        TokenService.delete_user_auth_token(user)
        return Response(status=status.HTTP_200_OK)


class DeleteUserAccountView(APIView):
    """View for deleting user account."""

    permission_classes = [IsAuthenticated]

    def delete(self, request) -> Response:
        """Deletes user account."""
        user = request.user
        TokenService.delete_user_auth_token(user)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateUserDataView(APIView):
    """View for updating user data."""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Update user data."""
        serializer = UpdateUserDateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        UserService.update_user_data(user, serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UsersListView(APIView):
    """View for getting users list."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Returns list of users."""
        users_list = self.__get_users_list()
        return Response(data=users_list, status=status.HTTP_200_OK)

    def __get_users_list(self) -> list:
        """Get queryset than serialize it and return users list."""
        queryset = User.objects.all()
        serializer = UsersListSerializer(queryset, many=True)
        return json.loads(json.dumps(serializer.data))


class UserChangeEmailView(APIView):
    """Class for changing user email."""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Writes new user email in not confirmed emails and
        sends message to new user email for confirmation email.
        """
        serializer = ChangeUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        new_user_email = serializer.data['new_user_email']
        NotConfirmedEmail(user=user, email=new_user_email).save()
        EmailService.send_email_for_confirm_changing_email(
            request, user, new_user_email)
        return Response(status=status.HTTP_200_OK)


class EmailConfirmationView(APIView):
    """Class for confirmation changing email."""

    def get(self, request, id, token):
        """Checks that given token is right and changes user email."""
        user = User.objects.get(id=id)
        not_confirmed_email = NotConfirmedEmail.objects.get(user=user)
        new_user_email = not_confirmed_email.email
        if TokenService.check_email_confirmation_token(
                token, user, new_user_email):

            user.email = new_user_email
            user.save()
            not_confirmed_email.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
