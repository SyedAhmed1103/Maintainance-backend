from django.db import models


class Payment(models.Model):

    PAYMENT_MODES = (
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    maintenance_detail = models.ForeignKey(
        'maintainancedetails.MaintenanceDetail',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    flat = models.ForeignKey(
        'flats.Flat',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODES
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']

    def __str__(self):
        return self.receipt_number