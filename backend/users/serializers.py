from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class SignUpSerializer(serializers.Serializer):
    """Serializer for user registration."""

    first_name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    username = serializers.CharField(
        max_length=30, validators=[UniqueValidator(
        queryset=User.objects.all())]
        )

    email = serializers.EmailField(
        max_length=50, validators=[UniqueValidator(
        queryset=User.objects.all())]
        )
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        """Check that first password equal second"""
        if data["password"] == data["password2"]:
            return data
        raise serializers.ValidationError("Passwords doesn't match")

    def validate_first_name(self, first_name):
        """Check that name doesn't contain 'bad' symbols"""
        s = "1234567890.?/,!@#$%^&*()_-+={}[]\|\\;:\"'<>"
        for letter in first_name.lower():
            if letter in s:
                raise serializers\
                    .ValidationError("Name must contain only latters.")
        return first_name

    def validate_surname(self, surname):
        """Check that surname doesn't contain 'bad' symbols"""
        s = "1234567890.?/,!@#$%^&*()_-+={}[]\|\\;:\"'<>"
        for letter in surname.lower():
            if letter in s:
                raise serializers\
                    .ValidationError("Surname must contain only latters.")
        return surname


class LogInSerializer(serializers.Serializer):
    """Serializer for login users."""
    username = serializers.CharField()
    password = serializers.CharField()


class UsersListSerializer(serializers.ModelSerializer):
    """Serializer for getting list of users."""
    class Meta:
        model = User
        fields = ('first_name', 'surname', 'username')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        """Check that first password equal second"""
        if data["new_password"] == data["new_password2"]:
            return data
        raise serializers.ValidationError("Passwords doesn't match")
