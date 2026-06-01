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

    total_floors = models.IntegerField(
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

    total_flats = models.IntegerField(
        default=0
    )

    building_type = models.CharField(
        max_length=20,
        choices=BUILDING_TYPES,
        default='residential'
    )

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='buildings'
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

    def __str__(self):
        return self.building_name
    
