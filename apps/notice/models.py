from django.db import models


class Notice(models.Model):

    building = models.ForeignKey(
        'building.Building',
        on_delete=models.CASCADE,
        related_name='notices'
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    start_date = models.DateField()

    end_date = models.DateField()

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
        db_table = 'notices'
        ordering = ['-created_at']

    def __str__(self):
        return self.title