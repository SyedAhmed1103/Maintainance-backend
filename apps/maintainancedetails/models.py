from django.db import models


class MaintenanceDetail(models.Model):

    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    )

    maintenance = models.ForeignKey(
        'maintenance.Maintenance',
        on_delete=models.CASCADE,
        related_name='maintenance_details'
    )

    flat = models.ForeignKey(
        'flats.Flat',
        on_delete=models.CASCADE,
        related_name='maintenance_details'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    late_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'maintenance_details'
        ordering = ['-created_at']
        unique_together = ('maintenance', 'flat')

    def __str__(self):
        return f"{self.flat} - {self.maintenance}"