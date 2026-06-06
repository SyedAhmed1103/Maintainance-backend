from django.db import models

from apps.building.models import Building


class Wing(models.Model):

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='wings'
    )

    wing_name = models.CharField(
        max_length=20
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

        db_table = 'wings'

        ordering = ['wing_name']

        constraints = [
            models.UniqueConstraint(
                fields=['building', 'wing_name'],
                name='unique_wing_per_building'
            )
        ]

    def __str__(self):

        return f"{self.building.building_name} - {self.wing_name}"