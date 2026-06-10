from django.db import models


class Building(models.Model):

    BUILDING_TYPES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    )

    building_name = models.CharField(
        max_length=255
    )

    building_code = models.CharField(
        max_length=50,
        unique=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    total_floors = models.PositiveIntegerField(
        default=0
    )

    society_email = models.EmailField(
        blank=True,
        null=True
    )

    society_mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    building_type = models.CharField(
        max_length=20,
        choices=BUILDING_TYPES,
        default='residential'
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
        db_table = 'buildings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['building_code']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.building_name} ({self.building_code})"