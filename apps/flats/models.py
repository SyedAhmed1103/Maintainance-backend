from django.db import models


class Flat(models.Model):

    OCCUPANCY_STATUS = (
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
        ('unsold', 'Unsold'),
    )

    FLAT_TYPES = (
        ('1RK', '1 RK'),
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('3BHK', '3 BHK'),
        ('4BHK', '4 BHK'),
        ('5BHK', '5 BHK'),
        ('SHOP', 'Shop'),
        ('OFFICE', 'Office'),
        ('COMMERCIAL', 'Commercial Unit'),
        ('WAREHOUSE', 'Warehouse'),
    )

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='flats'
    )

    wing = models.ForeignKey(
        'wing.Wing',
        on_delete=models.PROTECT,
        related_name='flats'
    )

    flat_number = models.CharField(
        max_length=20
    )

    floor_number = models.PositiveIntegerField()

    flat_type = models.CharField(
        max_length=20,
        choices=FLAT_TYPES
    )
    owner = models.ForeignKey(
    'users.User',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='flats'
    )

    occupancy_status = models.CharField(
        max_length=20,
        choices=OCCUPANCY_STATUS,
        default='unsold'
    )

    area_sqft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
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

        db_table = 'flats'

        ordering = [
            'wing__wing_name',
            'floor_number',
            'flat_number'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'building',
                    'wing',
                    'flat_number'
                ],
                name='unique_flat_per_wing'
            )
        ]

        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['wing']),
            models.Index(fields=['flat_number']),
            models.Index(fields=['occupancy_status']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):

        return (
            f"{self.wing.wing_name}"
            f"-{self.flat_number}"
        )