from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Cutom user model."""

    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )

    first_name = models.CharField(
        max_length=30, verbose_name="first name")

    surname = models.CharField(
        max_length=30, verbose_name="surname")

    username = models.CharField(
        max_length=30, verbose_name="username", unique=True)

    slug = models.SlugField(
        verbose_name="field intends for useing in url", unique=True)

    email = models.EmailField(
        max_length=50, verbose_name="user email", unique=True)

    age = models.PositiveIntegerField(blank=True, null=True,
                                      verbose_name="how old is user")

    gender = models.CharField(max_length=10, choices=GENDER,
                              blank=True, null=True)

    training_experience = models.DecimalField(
        max_digits=3, decimal_places=1,
        verbose_name="How long does user train in total",
        blank=True, null=True)

    trains_now = models.BooleanField(
        verbose_name="Does user train now", blank=True, null=True)

    is_staff = models.BooleanField(
        default=False, verbose_name="Is user a member of staff?")

    is_superuser = models.BooleanField(
        default=False, verbose_name="Is user a superuser?")

    is_active = models.BooleanField(default=True,
        verbose_name="Is user active of his account was deleted?")

    is_activated = models.BooleanField(
        default=False, verbose_name="Has user activated accoung?")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname', 'email']

    class Meta:
        ordering = ("username",)
        verbose_name_plural = "Users"
        verbose_name = "User"
