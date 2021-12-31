from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'surname', 'username', 'email', 'password')


class LogInSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')