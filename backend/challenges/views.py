from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

from .models import Challenge, ChallengeBalance
from .serializers import CreateChallengeSerializer
from .services.challenge_services import ChallengeService

from users.services.user_services import UserService


class CreateChallengeView(APIView):
    """View for creating challenge."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Creates challenge."""
        serializer = CreateChallengeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        current_user_challenge_with_same_name = Challenge.objects.all().filter(
            creator=user, name=serializer.data['name'])
        if current_user_challenge_with_same_name:
            data = {'message': 'user already has challenge with this name'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not UserService.has_user_enough_coins(user, serializer.data['bet']):
            data = {'message': 'user hasn\'t enough coinst for create challange'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            challenge = ChallengeService.create_challenge(serializer.data, user)
        except:
            data = {'message': 'creating challenge error'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        ChallengeBalance(challenge=challenge, coins_amount=challenge.bet).save()
        user.balance.coins_amount -= challenge.bet
        user.balance.save()

        return Response(status=status.HTTP_200_OK)


class UploadVideoExampleView(APIView):
    """View for upload video example for challenge."""

    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated]

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











