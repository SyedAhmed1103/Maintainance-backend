# apps/complaint/serializers.py

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Complaint

from apps.media_manager.models import Media
from apps.media_manager.serializers import MediaSerializer


class ComplaintSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source="building.name",
        read_only=True
    )

    flat_name = serializers.CharField(
        source="flat.flat_number",
        read_only=True
    )

    user_name = serializers.SerializerMethodField()

    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Complaint

        fields = (
            "id",

            "building",
            "building_name",

            "flat",
            "flat_name",

            "user",
            "user_name",

            "title",
            "description",

            "admin_remark",
            "status",

            "attachments",

            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",

            "building_name",
            "flat_name",
            "user_name",

            "admin_remark",
            "status",

            "attachments",

            "created_at",
            "updated_at",
        )

    def get_user_name(self, obj):

        if hasattr(obj.user, "get_full_name"):
            full_name = obj.user.get_full_name()

            if full_name:
                return full_name

        return str(obj.user)

    def get_attachments(self, obj):

        content_type = ContentType.objects.get_for_model(
            Complaint
        )

        attachments = Media.objects.filter(
            content_type=content_type,
            object_id=obj.id,
            category=Media.Category.COMPLAINT_ATTACHMENT,
            is_active=True,
        ).order_by(
            "display_order",
            "id"
        )

        return MediaSerializer(
            attachments,
            many=True,
            context=self.context,
        ).data

    def validate_title(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title is required."
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters."
            )

        return value

    def validate_description(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Description is required."
            )

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must be at least 10 characters."
            )

        return value

    def validate(self, attrs):

        building = attrs.get("building")
        flat = attrs.get("flat")

        if (
            building and
            flat and
            hasattr(flat, "building_id")
        ):
            if flat.building_id != building.id:
                raise serializers.ValidationError(
                    {
                        "flat":
                        "Selected flat does not belong to the selected building."
                    }
                )

        return attrs