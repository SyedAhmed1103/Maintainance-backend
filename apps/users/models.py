from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (
        ('owner', 'Owner'),
    )

    username = None

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True
    )

    mobile = models.CharField(
        max_length=15,
        unique=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='owner'
    )

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )


    is_verified = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['mobile']

    class Meta:

        db_table = 'users'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['mobile']),
            models.Index(fields=['user_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):

        return f"{self.first_name} {self.last_name or ''}".strip()

    @property
    def full_name(self):

        return f"{self.first_name} {self.last_name or ''}".strip()