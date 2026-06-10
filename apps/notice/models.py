from django.db import models
from django.core.exceptions import ValidationError


class Notice(models.Model):

    class NoticeType(models.TextChoices):
        GENERAL = "general", "General"
        MAINTENANCE = "maintenance", "Maintenance"
        MEETING = "meeting", "Meeting"
        EVENT = "event", "Event"
        EMERGENCY = "emergency", "Emergency"

    building = models.ForeignKey(
        "building.Building",
        on_delete=models.CASCADE,
        related_name="notices",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    notice_type = models.CharField(
        max_length=20,
        choices=NoticeType.choices,
        default=NoticeType.GENERAL,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_notices",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "notices"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=["building"]
            ),
            models.Index(
                fields=["notice_type"]
            ),
            models.Index(
                fields=["is_active"]
            ),
            models.Index(
                fields=["start_date"]
            ),
            models.Index(
                fields=["end_date"]
            ),
        ]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                {
                    "end_date":
                    "End date cannot be before start date."
                }
            )

    @property
    def is_currently_visible(self):
        from django.utils import timezone

        today = timezone.localdate()

        return (
            self.is_active
            and self.start_date <= today
            and self.end_date >= today
        )

    def __str__(self):
        return (
            f"{self.title}"
            f" ({self.building.name})"
        )