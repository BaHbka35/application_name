import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

from .models import Challenge, ChallengeBalance, ChallengeMember
from .serializers import CreateChallengeSerializer, GetChallengesListSerializer,\
                         GetDitailChallengeInfoSerializer
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
        user = request.user
        challenge = Challenge.objects.get(id=challenge_id)

        if not challenge.creator == user:
            data = {'message': 'You can\'t upload video. You aren\'t creator.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not ChallengeService.is_video_example_file_valid(request.data):
            data = {'message': 'video file not valid.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        video_example_file = request.data['video_example']
        ChallengeService.update_video_example(user, challenge,
                                              video_example_file)
        return Response(status=status.HTTP_200_OK)


class AcceptChallengeView(APIView):
    """View for accept challenge by user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id: int) -> Response:
        """Makes the user a member of challenge."""
        challenge = Challenge.objects.get(id=challenge_id)
        user = request.user

        if not challenge.is_active:
            data = {'message': 'this challenge was finished.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if ChallengeMember.objects.all().filter(user=user, challenge=challenge):
            data = {'message': 'user have already accepted this challenge'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not UserService.has_user_enough_coins(user, challenge.bet):
            data = {'message': 'user hasn\'t enough coins for accept challenge'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        ChallengeMember(user=user, challenge=challenge).save()
        if not ChallengeService.is_challenge_free(challenge):
            UserService.withdraw_coins_from_user(user, challenge.bet)
            ChallengeService.add_coins_for_challenge(challenge, challenge.bet)

        return Response(status=status.HTTP_200_OK)


class GetChallengesListView(APIView):
    """View for getting active challenges list."""

    def get(self, request):
        """Returns list of active challenges."""
        queryset = Challenge.objects.all().filter(is_active=True)
        serializer = GetChallengesListSerializer(queryset, many=True)
        challenges_list = json.loads(json.dumps(serializer.data))
        return Response(data=challenges_list, status=status.HTTP_200_OK)


class GetDetailChallenge(APIView):
    """View for getting detail information about specific challenge."""

    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id: int):
        """Return detail information about challenge."""
        try:
            queryset = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            data = {'message': 'There isn\'t challenge with given id'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        serializer = GetDitailChallengeInfoSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)









