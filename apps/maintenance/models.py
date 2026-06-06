from django.db import models

from apps.building.models import Building
from apps.flats.models import Flat
from django.core.exceptions import ValidationError

# =========================================================
# MAINTENANCE CONFIG
# =========================================================

class MaintenanceConfig(models.Model):

    CALCULATION_TYPES = (
        ('fixed', 'Fixed'),
        ('per_sqft', 'Per Sqft'),
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='maintenance_configs'
    )

    calculation_type = models.CharField(
        max_length=20,
        choices=CALCULATION_TYPES
    )

    fixed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    rate_per_sqft = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    effective_from = models.DateField()

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

        db_table = 'maintenance_configs'

        ordering = ['-effective_from']

        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['effective_from']),
            models.Index(fields=['is_active']),
        ]

    def clean(self):

        if self.calculation_type == 'fixed':

            if not self.fixed_amount:

                raise ValidationError(
                    "Fixed amount is required."
                )

            self.rate_per_sqft = None

        elif self.calculation_type == 'per_sqft':

            if not self.rate_per_sqft:

                raise ValidationError(
                    "Rate per sqft is required."
                )

            self.fixed_amount = None

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.building.building_name} - "
            f"{self.calculation_type}"
        )
    
# =========================================================
# MAINTENANCE BILL
# =========================================================

class MaintenanceBill(models.Model):

    BILL_TYPES = (
        ('opening', 'Opening Due'),
        ('monthly', 'Monthly Maintenance'),
        ('special', 'Special Charge'),
    )

    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    )

    flat = models.ForeignKey(
        Flat,
        on_delete=models.CASCADE,
        related_name='maintenance_bills'
    )

    bill_type = models.CharField(
        max_length=20,
        choices=BILL_TYPES,
        default='monthly'
    )

    month = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    pending_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    due_date = models.DateField()

    generated_on = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid'
    )

    notes = models.TextField(
        blank=True,
        null=True
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

        db_table = 'maintenance_bills'

        ordering = [
            '-year',
            '-month',
            '-created_at'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'flat',
                    'bill_type',
                    'month',
                    'year'
                ],
                name='unique_bill_per_month'
            )
        ]

        indexes = [
            models.Index(fields=['flat']),
            models.Index(fields=['status']),
            models.Index(fields=['year']),
            models.Index(fields=['month']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):

        if self.bill_type == 'monthly':

            return (
                f"{self.flat.flat_number} "
                f"{self.month}/{self.year}"
            )

        return (
            f"{self.flat.flat_number} "
            f"{self.bill_type}"
        )


# =========================================================
# PAYMENT
# =========================================================

class Payment(models.Model):

    PAYMENT_MODES = (
        ('online', 'Online'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    )

    flat = models.ForeignKey(
        Flat,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    unallocated_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
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

    remarks = models.TextField(
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField()

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

        db_table = 'payments'

        ordering = ['-paid_at']

        indexes = [
            models.Index(fields=['flat']),
            models.Index(fields=['receipt_number']),
            models.Index(fields=['paid_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):

        return (
            f"{self.flat.flat_number} - "
            f"{self.amount}"
        )


# =========================================================
# PAYMENT ADJUSTMENT
# =========================================================

class PaymentAdjustment(models.Model):

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='adjustments'
    )

    bill = models.ForeignKey(
        MaintenanceBill,
        on_delete=models.CASCADE,
        related_name='adjustments'
    )

    adjusted_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = 'payment_adjustments'

        indexes = [
            models.Index(fields=['payment']),
            models.Index(fields=['bill']),
        ]

    def __str__(self):

        return (
            f"{self.payment.id} -> "
            f"{self.bill.id}"
        )