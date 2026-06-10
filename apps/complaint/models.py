from django.db import models


class Complaint(models.Model):

    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )

    building = models.ForeignKey(
        "building.Building",
        on_delete=models.CASCADE,
        related_name="complaints",
        db_index=True,
    )

    flat = models.ForeignKey(
        "flats.Flat",
        on_delete=models.CASCADE,
        related_name="complaints",
        db_index=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    admin_remark = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        db_index=True,
    )

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "complaints"

        ordering = [
            "-created_at"
        ]

        indexes = [
            models.Index(fields=["building"]),
            models.Index(fields=["flat"]),
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"#{self.id} - {self.title}"