from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, GENDER


def validate_first_name(first_name: str) -> str:
    """Check that name doesn't contain 'bad' symbols"""
    s = "1234567890.?/,!@#$%^&*()_-+={}[]\|\\;:\"'<>"
    for letter in first_name.lower():
        if letter in s:
            raise serializers\
                .ValidationError('Name must contain only letters.')
    return first_name


def validate_surname(surname: str) -> str:
    """Check that surname doesn't contain 'bad' symbols"""
    s = "1234567890.?/,!@#$%^&*()_-+={}[]\|\\;:\"'<>"
    for letter in surname.lower():
        if letter in s:
            raise serializers\
                .ValidationError('Surname must contain only letters.')
    return surname


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

    def validate(self, data: dict) -> dict:
        """Check that first password equal second"""
        if data['password'] == data['password2']:
            return data
        raise serializers.ValidationError('Passwords doesn\'t match')

    def validate_first_name(self, first_name: str) -> str:
        """Check that name doesn't contain 'bad' symbols"""
        return validate_first_name(first_name)

    def validate_surname(self, surname: str) -> str:
        """Check that surname doesn't contain 'bad' symbols"""
        return validate_surname(surname)


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

    def validate(self, data: dict) -> dict:
        """Check that first password equal second"""
        if data['new_password'] == data['new_password2']:
            return data
        raise serializers.ValidationError('Passwords doesn\'t match')


class UpdateUserDateSerializer(serializers.Serializer):
    """Serializer for updating user data."""
    first_name = serializers.CharField(max_length=30, required=True)
    surname = serializers.CharField(max_length=30, required=True)
    username = serializers.CharField(
        max_length=30, validators=[UniqueValidator(
            queryset=User.objects.all())], required=True
        )
    age = serializers.IntegerField(min_value=1, required=True)
    gender = serializers.ChoiceField(choices=GENDER, required=True)
    training_experience = serializers.DecimalField(
        min_value=0, max_digits=3, decimal_places=1, required=True)
    trains_now = serializers.BooleanField(required=True)

    def validate_first_name(self, first_name: str) -> str:
        """Check that name doesn't contain 'bad' symbols"""
        return validate_first_name(first_name)

    def validate_surname(self, surname: str) -> str:
        """Check that surname doesn't contain 'bad' symbols"""
        return validate_surname(surname)

    def validate_training_experience(self, training_experience: str) -> str:
        """Check that training_experience is positive or null"""
        if training_experience >= 0:
            return training_experience
        raise serializers.ValidationError(
            'Training experience must be positive of null')


class ChangeUserEmailSerializer(serializers.Serializer):
    """Serializer for changing user email."""
    new_user_email = serializers.EmailField(required=True, max_length=50)

    def validate_new_user_email(self, new_user_email: str) -> str:
        """Checks that new user email is not using other user."""
        try:
            User.objects.get(email=new_user_email)
        except User.DoesNotExist:
            return new_user_email
        raise serializers.ValidationError('This email is already using')