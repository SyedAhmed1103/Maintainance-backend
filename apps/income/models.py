from django.db import models


class Income(models.Model):

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='incomes'
    )

    income_type = models.CharField(
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

    income_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'incomes'
        ordering = ['-income_date']

    def __str__(self):
        return f"{self.income_type} - {self.amount}"