from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Challenge


class CreateChallengeSerializer(serializers.Serializer):
    """Serializer for creating challenge."""

    name = serializers.CharField(
        max_length=200,
        validators=[
            UniqueValidator(queryset=Challenge.objects.all())
            ]
        )
    date_finish = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    goal = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    requirements = serializers.CharField(max_length=500)
    bet = serializers.IntegerField(min_value=0)
