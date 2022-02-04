import datetime

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Challenge
from users.models import User
from .serializers import CreateChallengeSerializer
from .services.challenge_services import ChallengeService


class CreateChallengeView(APIView):
    """View for creating challange."""

    permitions = [IsAuthenticated]

    def post(self, request) -> Response:
        """Creates challenge."""
        serializer = CreateChallengeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        current_user_challenge_with_same_name = Challenge.objects.all().filter(
            creator=user, name=serializer.data['name'])
        if current_user_challenge_with_same_name:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            ChallengeService.create_challenge(serializer.data, user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
