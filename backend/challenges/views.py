import datetime
import os

from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

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


class UploadVideoExampleView(APIView):
    """View for upload video example for challenge."""

    parser_class = [FileUploadParser]
    permitions = [IsAuthenticated]

    def put(self, request, challenge_id: int) -> Response:
        """"""
        if 'video_example' not in request.data:
            if not request.data['video_example']:
                data={'message': 'there isn\' video file.'},
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['video_example'].temporary_file_path()[-3:] == 'mp4':
            data={'message': 'video format not mp4'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        challenge = Challenge.objects.get(id=challenge_id)
        file_name = f'{user.id}_{challenge.id}.mp4'
        if challenge.video_example:
            os.remove(os.path.join(settings.MEDIA_ROOT, f'video_examples/{file_name}'))
        file_name = f'{user.id}_{challenge.id}.mp4'
        challenge.video_example = request.data['video_example']
        challenge.video_example.name = file_name
        challenge.save()

        return Response(status=status.HTTP_200_OK)












