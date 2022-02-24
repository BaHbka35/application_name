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

from .services.email_services import EmailAddressHandlingService
from .services.token_services import ActivationTokenService,\
                                     AuthenticationTokenService,\
                                     EmailConfirmationTokenService
from .services.user_services import UserService
from .services.token_signature_services import TokenSignatureService
from .services import services

from .tasks import send_email_for_activate_account,\
                   send_email_for_confirm_changing_email


class SignUpView(APIView):
    """View for registration user."""

    def post(self, request) -> Response:
        """
        Registrate user and send email for account activation.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user_and_his_balance(serializer.data)
        send_email_for_activate_account.delay(
            services.get_current_site_domain(request), user.id)
        data = services.get_amended_data_for_response_from_signup_view(
            serializer.data)
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

        result, data = ActivationTokenService.is_activation_token_valid(
            user, encrypted_datetime, token)
        if not result:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_activated:
            data = {'message': 'User is not activated'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        token = AuthenticationTokenService.get_user_authentication_token(user)
        signature = TokenSignatureService.get_signature(token)
        data = {'token': token, 'signature': signature}
        return Response(data=data, status=status.HTTP_200_OK)


class LogOutView(APIView):
    """View for logs user out."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Logs user out."""
        user = request.user
        AuthenticationTokenService.delete_user_authentication_token(user)
        data = {'message': 'User was successfully logout'}
        return Response(data=data, status=status.HTTP_200_OK)


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
        AuthenticationTokenService.delete_user_authentication_token(user)
        data = {'message': 'User password was changed successfully.'}
        return Response(data=data, status=status.HTTP_200_OK)


class DeleteUserAccountView(APIView):
    """View for deleting user account."""

    permission_classes = [IsAuthenticated]

    def delete(self, request) -> Response:
        """Deletes user account."""
        request.user.delete()
        data = {'message': 'User was deleted successfully.'}
        return Response(data=data, status=status.HTTP_200_OK)


class UpdateUserDataView(APIView):
    """View for updating user data."""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Updates user data."""
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
        users_queryset = User.objects.all()
        serializer = UsersListSerializer(users_queryset, many=True)
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
        EmailAddressHandlingService.add_email_address_to_not_confirmed(
            user, new_user_email)
        send_email_for_confirm_changing_email.delay(
            services.get_current_site_domain(request), user.id, new_user_email)
        return Response(status=status.HTTP_200_OK)


class EmailConfirmationView(APIView):
    """Class for confirmation changing email."""

    def get(self, request, id: int, encrypted_datetime: str, token: str) -> Response:
        """Checks that given token is right and changes user email."""
        user = User.objects.get(id=id)
        not_confirmed_email = NotConfirmedEmail.objects.get(user=user)
        new_user_email = not_confirmed_email.email

        result, data = EmailConfirmationTokenService.is_email_confirmation_token_valid(
            user, encrypted_datetime, token,  new_user_email)
        if not result:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        user.email = new_user_email
        user.save()
        not_confirmed_email.delete()
        return Response(status=status.HTTP_200_OK)









