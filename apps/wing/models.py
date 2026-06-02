from django.db import models
from apps.building.models import Building


class Wing(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='wings'
    )
    wing_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.building.building_name} - {self.wing_name}"