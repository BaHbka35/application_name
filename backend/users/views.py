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

from .models import User, NotConfirmedEmail, UserBalance

from .services.email_services import EmailService
from .services.token_services import TokenService
from .services.user_services import UserService
from .services.token_signature_services import TokenSignatureService
from .services.datetime_services import DatetimeService


class SignUpView(APIView):
    """View for registration user."""

    def post(self, request) -> Response:
        """
        Registrate user and send email for account activation.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.data)
        UserBalance(user=user).save()
        EmailService.send_email_for_activate_account(request, user)

        data = serializer.data
        data["message"] = "Check your email for activate account."
        del data['password']
        return Response(data=data, status=status.HTTP_201_CREATED)


class AccountActivationView(APIView):
    """View for activate user account."""

    def get(self, request, id: int, encrypted_datetime: str, token: str) -> Response:
        """Activate user."""
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            data = {'message': 'Activation account is failed.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        decrypted_datetime = DatetimeService.get_decrypted_datetime(encrypted_datetime)
        if not TokenService.check_token_lifetime(decrypted_datetime):
            data = {'message': 'Lifetime of token is finished.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not TokenService.check_activation_token(user, encrypted_datetime, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        UserService.activate_user(user)
        data = {'message': 'User was successfully activated.'}
        return Response(data=data, status=status.HTTP_200_OK)


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
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.data['username'],
                            password=serializer.data['password'])
        if not user:
            data = {'message': 'Username or password incorrect.'}
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.is_activated:
            data = {'message': 'User is not activated'}
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
        token = TokenService.get_user_auth_token(user)
        signature = TokenSignatureService.get_signature(token)
        data = {'token': token, 'signature': signature}
        return Response(data=data, status=status.HTTP_200_OK)


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
            user, serializer.data['new_password'])
        TokenService.delete_user_auth_token(user)
        return Response(status=status.HTTP_200_OK)


class DeleteUserAccountView(APIView):
    """View for deleting user account."""

    permission_classes = [IsAuthenticated]

    def delete(self, request) -> Response:
        """Deletes user account."""
        request.user.delete()
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
        queryset = User.objects.all()
        serializer = UsersListSerializer(queryset, many=True)
        users_list = json.loads(json.dumps(serializer.data))
        return Response(data=users_list, status=status.HTTP_200_OK)


class UserChangeEmailView(APIView):
    """Class for changing user email."""

    permission_classes = [IsAuthenticated]

    def put(self, request) -> Response:
        """
        Writes new user email in not confirmed emails and sends
        message to new user email with confirmation link.
        """
        serializer = ChangeUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        new_user_email = serializer.data['new_user_email']
        EmailService.add_email_to_not_confirmed(user, new_user_email)
        EmailService.send_email_for_confirm_changing_email(
            request, user, new_user_email)
        return Response(status=status.HTTP_200_OK)


class EmailConfirmationView(APIView):
    """Class for confirmation changing email."""

    def get(self, request, id: int, encrypted_datetime: str, token: str) -> Response:
        """Checks that given token is right and changes user email."""
        user = User.objects.get(id=id)
        not_confirmed_email = NotConfirmedEmail.objects.get(user=user)
        new_user_email = not_confirmed_email.email

        decrypted_datetime = DatetimeService.get_decrypted_datetime(encrypted_datetime)
        if not TokenService.check_token_lifetime(decrypted_datetime):
            data = {'message': 'Lifetime of token is finished.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not TokenService.is_email_confirmation_token_belongs_to_current_user(
                user, encrypted_datetime, token,  new_user_email):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user.email = new_user_email
        user.save()
        not_confirmed_email.delete()
        return Response(status=status.HTTP_200_OK)









