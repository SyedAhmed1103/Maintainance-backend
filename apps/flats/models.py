from django.db import models


class Flat(models.Model):

    OCCUPANCY_STATUS = (
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
    )

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='flats'
    )

    wing = models.CharField(
        max_length=10
    )

    flat_number = models.CharField(
        max_length=20
    )

    floor_number = models.PositiveIntegerField()

    flat_type = models.CharField(
        max_length=50
    )

    occupancy_status = models.CharField(
        max_length=10,
        choices=OCCUPANCY_STATUS,
        default='vacant'
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
        ordering = ['wing', 'flat_number']
        unique_together = ('building', 'wing', 'flat_number')

    def __str__(self):
        return f"{self.wing}-{self.flat_number}"