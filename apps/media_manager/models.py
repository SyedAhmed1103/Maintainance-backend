# apps/media_manager/models.py

import os
import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def media_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()

    return (
        f"{instance.content_type.model}s/"
        f"{instance.object_id}/"
        f"{instance.category}/"
        f"{uuid.uuid4().hex}{ext}"
    )


class Media(models.Model):

    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        DOCUMENT = "document", "Document"

    class Category(models.TextChoices):
        AVATAR = "avatar", "Avatar"

        BUILDING_IMAGE = (
            "building_image",
            "Building Image"
        )

        COMPLAINT_ATTACHMENT = (
            "complaint_attachment",
            "Complaint Attachment"
        )

        NOTICE_ATTACHMENT = (
            "notice_attachment",
            "Notice Attachment"
        )

    # Generic Relation

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveBigIntegerField()

    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    # Media Info

    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices
    )

    category = models.CharField(
        max_length=50,
        choices=Category.choices
    )

    file = models.FileField(
        upload_to=media_upload_path
    )

    # Metadata

    original_name = models.CharField(
        max_length=255
    )

    mime_type = models.CharField(
        max_length=100,
        blank=True
    )

    file_size = models.BigIntegerField(
        default=0
    )

    # For Multiple Images Ordering

    display_order = models.PositiveIntegerField(
        default=0
    )

    # Status

    is_active = models.BooleanField(
        default=True
    )

    # Audit

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "media"

        ordering = [
            "display_order",
            "-created_at"
        ]

        indexes = [
            models.Index(
                fields=[
                    "content_type",
                    "object_id"
                ]
            ),
            models.Index(
                fields=["category"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.category} - "
            f"{self.original_name}"
        )

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None