from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

from .models import Challenge
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
        if not ChallengeService.is_video_example_file_valid(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        video_example_file = request.data['video_example']
        user = request.user
        challenge = Challenge.objects.get(id=challenge_id)

        ChallengeService.update_video_example(user, challenge,
                                                video_example_file)

        return Response(status=status.HTTP_200_OK)











