from django.db import models


class Maintenance(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('completed', 'Completed'),
    )

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='maintenances'
    )

    title = models.CharField(
        max_length=255
    )

    generated_date = models.DateField()

    month = models.PositiveSmallIntegerField()

    year = models.PositiveIntegerField()

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='generated'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'maintenances'
        ordering = ['-year', '-month']
        unique_together = ('building', 'month', 'year')

    def __str__(self):
        return f"{self.title} ({self.month}/{self.year})"