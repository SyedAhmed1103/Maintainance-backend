from django.db import models
from django.core.exceptions import ValidationError


class FlatType(models.Model):

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='flat_types'
    )

    name = models.CharField(
        max_length=50
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

        db_table = 'flat_types'

        ordering = [
            'name'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'building',
                    'name'
                ],
                name='unique_flat_type_per_building'
            )
        ]

        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):

        return self.name


class Flat(models.Model):

    OCCUPANCY_STATUS = (
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
        ('unsold', 'Unsold'),
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

    flat_type = models.ForeignKey(
        FlatType,
        on_delete=models.PROTECT,
        related_name='flats'
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
            models.Index(fields=['flat_type']),
        ]

    def clean(self):

        if (
            self.flat_type
            and self.building
            and self.flat_type.building_id != self.building_id
        ):
            raise ValidationError(
                {
                    'flat_type':
                    'Selected flat type does not belong to the selected building.'
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.wing.wing_name}"
            f"-{self.flat_number}"
        )