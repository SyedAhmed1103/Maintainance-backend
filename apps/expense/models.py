from django.db import models


class Expense(models.Model):

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    expense_type = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    expense_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'expenses'
        ordering = ['-expense_date']

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"