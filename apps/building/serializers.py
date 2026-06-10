from rest_framework import serializers

from .models import Building
from django.contrib.contenttypes.models import ContentType

from apps.media_manager.models import Media
from apps.media_manager.serializers import MediaSerializer

class PublicBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            "id",
            "building_name",
        ]

class BuildingSerializer(serializers.ModelSerializer):

    building_image = serializers.SerializerMethodField()


    class Meta:
        model = Building

        fields = [
            'id',
            'building_name',
            'building_code',
            'address',
            'city',
            'state',
            'pincode',
            'total_floors',
            'society_email',
            'society_mobile',
            'building_type',
            'building_image',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'building_image',
            
        ]

    # ==========================================
    # CUSTOM METHODS
    # ==========================================


    def get_building_image(self, obj):

        content_type = (
            ContentType.objects.get_for_model(
                Building
            )
        )

        media = Media.objects.filter(
            content_type=content_type,
            object_id=obj.id,
            category=Media.Category.BUILDING_IMAGE,
            is_active=True,
        ).first()

        if not media:
            return None

        return MediaSerializer(
            media,
            context=self.context,
        ).data

    # ==========================================
    # FIELD VALIDATIONS
    # ==========================================

    def validate_building_name(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Building name must be at least 3 characters long."
            )

        return value.title()

    def validate_building_code(self, value):

        value = value.strip().upper()

        queryset = Building.objects.filter(
            building_code__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Building code already exists."
            )

        return value

    def validate_city(self, value):

        return value.strip().title()

    def validate_state(self, value):

        return value.strip().title()

    def validate_pincode(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Pincode must contain only numbers."
            )

        if len(value) != 6:
            raise serializers.ValidationError(
                "Pincode must be exactly 6 digits."
            )

        return value

    def validate_total_floors(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Total floors cannot be negative."
            )

        return value

    def validate_society_mobile(self, value):

        if not value:
            return value

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if not (10 <= len(value) <= 15):
            raise serializers.ValidationError(
                "Mobile number must be between 10 and 15 digits."
            )

        return value

    def validate_address(self, value):

        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Address is too short."
            )

        return value