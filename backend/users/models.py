from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


GENDER = (
    ('male', 'male'),
    ('female', 'female'),
)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    first_name = models.CharField(
        max_length=30, verbose_name='first name')

    surname = models.CharField(
        max_length=30, verbose_name='surname')

    username = models.CharField(
        max_length=30, verbose_name='username', unique=True)

    slug = models.SlugField(
        verbose_name='field intends for using in url (slug)', unique=True)

    email = models.EmailField(
        max_length=50, verbose_name='user email', unique=True)

    age = models.PositiveIntegerField(blank=True, null=True,
                                      verbose_name='how old is user')

    gender = models.CharField(max_length=10, choices=GENDER,
                              blank=True, null=True)

    training_experience = models.DecimalField(
        max_digits=3, decimal_places=1,
        verbose_name='How long does user train in total',
        blank=True, null=True)

    trains_now = models.BooleanField(
        verbose_name='Does user train now', blank=True, null=True)

    registration_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Date when user was registered')

    is_staff = models.BooleanField(
        default=False, verbose_name='Is user a member of staff?')

    is_superuser = models.BooleanField(
        default=False, verbose_name='Is user a superuser?')

    is_active = models.BooleanField(
        default=True, verbose_name='Is user active or his account was deleted?')

    is_activated = models.BooleanField(
        default=False, verbose_name='Has user activated account?')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname', 'email']

    class Meta:
        ordering = ('username',)
        verbose_name_plural = 'Users'
        verbose_name = 'User'


class NotConfirmedEmail(models.Model):
    """
    This model is needed for temporary store email addresses
    that users want to set instead old email addresses.
    Stores only not confirmed emails. If email
    is confirmed it must be deleted from here.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(
        max_length=50, verbose_name='email that user not confirmed')


class UserBalance(models.Model):
    """User balance"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True,
                                related_name='balance')
    coins_amount = models.PositiveIntegerField(verbose_name='coins amount',
                                               default=0)
