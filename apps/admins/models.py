from django.db import models


class Admin(models.Model):

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='admins'
    )

    name = models.CharField(
        max_length=255
    )

    mobile = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=255
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

    class Meta:
        db_table = 'admins'
        ordering = ['-created_at']

    def __str__(self):
        return self.name