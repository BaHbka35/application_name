from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

from .models import Challenge, ChallengeBalance, ChallengeMember
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
            data = {'message': 'user hasn\'t enough coins for create challenge'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            challenge = ChallengeService.create_challenge(serializer.data, user)
        except:
            data = {'message': 'creating challenge error'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        ChallengeBalance(challenge=challenge, coins_amount=challenge.bet).save()
        UserService.withdraw_coins_from_user(user, challenge.bet)
        ChallengeMember(user=user, challenge=challenge).save()

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


class AcceptChallengeView(APIView):
    """View for accept challenge by user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id: int) -> Response:
        """Makes user member of challenge."""
        challenge = Challenge.objects.get(id=challenge_id)
        user = request.user

        if ChallengeMember.objects.all().filter(user=user, challenge=challenge):
            data = {'message': 'user have already accepted this challenge'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not UserService.has_user_enough_coins(user, challenge.bet):
            data = {'message': 'user hasn\'t enough coins for accept challenge'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        ChallengeMember(user=user, challenge=challenge).save()
        if not challenge.is_free:
            UserService.withdraw_coins_from_user(user, challenge.bet)
            ChallengeService.add_coins_for_challenge(challenge, challenge.bet)

        return Response(status=status.HTTP_200_OK)







