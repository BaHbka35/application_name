from rest_framework import serializers
from rest_framework.validators import UniqueValidator,\
                                      UniqueTogetherValidator

from .models import User


class SignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        """Chack that first password equal second"""
        if data["password"] == data["password2"]:
            del data["password2"]
            return data
        raise serializer.ValidationError("Passwords doesn't match")

    def create(self, data):
        """ Creates and returns user"""
        return User.objects.create_user(**data)

    class Meta:

        # Needs for checking that there 
        # are no users with given username or email
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]
