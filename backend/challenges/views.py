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
        """Set video example for challenge."""
        if not self.__validate_video_file(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        video_example_file = request.data['video_example']
        user = request.user
        challenge = Challenge.objects.get(id=challenge_id)

        self.__update_video_exemple(user, challenge, video_example_file)

        return Response(status=status.HTTP_200_OK)

    def __validate_video_file(self, data):
        """Validates video file."""
        if 'video_example' not in data:
            return False
        if not data['video_example']:
            return False
        if not data['video_example'].temporary_file_path()[-3:] == 'mp4':
            return False
        return True

    def __update_video_exemple(self, user: User, challenge: Challenge,
                               video_example_file: '') -> Challenge:
        """Updates video example for challenge."""
        file_name = f'{user.id}_{challenge.id}.mp4'
        if challenge.video_example:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, f'video_examples/{file_name}'))
            except FileNotFoundError:
                pass

        challenge.video_example = video_example_file
        challenge.video_example.name = file_name
        challenge.save()
        return challenge











