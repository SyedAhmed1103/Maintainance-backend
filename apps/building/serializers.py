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
            'total_flats',
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

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_created_by_name(self, obj):

        if obj.created_by:

            full_name = obj.created_by.get_full_name()

            if full_name:
                return full_name

            return obj.created_by.username

        return None

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

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
                id=self.instance.id
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

    def validate_total_flats(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Total flats cannot be negative."
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

        if len(value) < 10 or len(value) > 15:

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

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        total_floors = attrs.get(
            'total_floors',
            self.instance.total_floors if self.instance else 0
        )

        total_flats = attrs.get(
            'total_flats',
            self.instance.total_flats if self.instance else 0
        )

        if total_flats > 0 and total_floors == 0:

            raise serializers.ValidationError({
                "total_floors": (
                    "Total floors must be greater than 0."
                )
            })

        return attrs