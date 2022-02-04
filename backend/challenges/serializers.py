import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Challenge


class CreateChallengeSerializer(serializers.Serializer):
    """Serializer for creating challenge."""

    name = serializers.CharField(max_length=200)
    finish_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    goal = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    requirements = serializers.CharField(max_length=500)
    bet = serializers.IntegerField(min_value=0)

    def validate_finish_datetime(self, finish_datetime):
        """Checks that finish_datetime > current_datetime."""
        if finish_datetime > datetime.datetime.now():
            return finish_datetime
        raise serializers.ValidationError('This is past datetime.')
