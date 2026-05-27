from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (
        ('admin', 'Admin'),
        ('resident', 'Resident'),
        ('owner', 'Owner'),
    )

    username = None

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='resident'
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    reset_token = models.TextField(
        blank=True,
        null=True
    )

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email