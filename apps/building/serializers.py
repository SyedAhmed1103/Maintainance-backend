from rest_framework import serializers

from .models import Building


class BuildingSerializer(serializers.ModelSerializer):

    created_by_name = serializers.SerializerMethodField()

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
            'created_by',
            'created_by_name',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
        ]

    # ==========================================
    # CUSTOM METHODS
    # ==========================================

    def get_created_by_name(self, obj):

        if not obj.created_by:
            return None

        full_name = obj.created_by.get_full_name()

        return full_name or obj.created_by.username

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