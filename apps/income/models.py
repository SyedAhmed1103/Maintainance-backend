from django.db import models
from django.core.validators import MinValueValidator


class Income(models.Model):

    building = models.ForeignKey(
        "building.Building",
        on_delete=models.CASCADE,
        related_name="incomes",
        db_index=True
    )

    income_type = models.CharField(
        max_length=100,
        db_index=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    description = models.TextField(
        blank=True
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    income_date = models.DateField(
        db_index=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "incomes"
        ordering = ["-income_date", "-id"]
        indexes = [
            models.Index(fields=["building", "income_date"]),
            models.Index(fields=["income_type"]),
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self):
        return f"{self.income_type} - {self.amount}"