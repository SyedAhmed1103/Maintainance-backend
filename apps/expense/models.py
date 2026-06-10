from django.db import models
from django.core.validators import MinValueValidator


class Expense(models.Model):

    building = models.ForeignKey(
        "building.Building",
        on_delete=models.CASCADE,
        related_name="expenses",
        db_index=True
    )

    expense_type = models.CharField(
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

    expense_date = models.DateField(
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
        db_table = "expenses"
        ordering = ["-expense_date", "-id"]
        indexes = [
            models.Index(fields=["building", "expense_date"]),
            models.Index(fields=["expense_type"]),
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"