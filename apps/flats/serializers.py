from rest_framework import serializers

from .models import Flat


class FlatSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Flat

        fields = [
            'id',
            'building',
            'building_name',
            'wing',
            'flat_number',
            'floor_number',
            'flat_type',
            'occupancy_status',
            'area_sqft',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'building_name',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_wing(self, value):

        value = value.strip().upper()

        if len(value) < 1:

            raise serializers.ValidationError(
                "Wing is required."
            )

        return value

    def validate_flat_number(self, value):

        value = value.strip().upper()

        if len(value) < 1:

            raise serializers.ValidationError(
                "Flat number is required."
            )

        return value

    def validate_floor_number(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Floor number cannot be negative."
            )

        return value

    def validate_flat_type(self, value):

        value = value.strip().title()

        if len(value) < 1:

            raise serializers.ValidationError(
                "Flat type is required."
            )

        return value

    def validate_area_sqft(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Area cannot be negative."
            )

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        building = attrs.get(
            'building',
            self.instance.building if self.instance else None
        )

        wing = attrs.get(
            'wing',
            self.instance.wing if self.instance else None
        )

        flat_number = attrs.get(
            'flat_number',
            self.instance.flat_number if self.instance else None
        )

        queryset = Flat.objects.filter(
            building=building,
            wing__iexact=wing,
            flat_number__iexact=flat_number
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError({
                "flat_number":
                "Flat already exists in this wing."
            })

        return attrs