from rest_framework import serializers

from .models import Flat


class FlatSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    wing_name = serializers.CharField(
        source='wing.wing_name',
        read_only=True
    )

    owner = serializers.SerializerMethodField()

    class Meta:

        model = Flat

        fields = [
            'id',

            'building',
            'building_name',

            'wing',
            'wing_name',

            'flat_number',
            'floor_number',

            'flat_type',

            'owner',

            'occupancy_status',

            'area_sqft',

            'is_active',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'building_name',
            'wing_name',
            'owner',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # OWNER DETAILS
    # ==================================================

    def get_owner(self, obj):

        if not obj.owner:

            return None

        return {
            "id": obj.owner.id,
            "full_name": obj.owner.full_name,
            "email": obj.owner.email,
            "mobile": obj.owner.mobile,
        }

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_flat_number(self, value):

        value = value.strip().upper()

        if not value:

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

    def validate_area_sqft(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Area must be greater than zero."
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

        # Wing belongs to Building

        if wing and building:

            if wing.building_id != building.id:

                raise serializers.ValidationError({
                    "wing":
                    "Selected wing does not belong to selected building."
                })

        # Unique Flat Per Wing

        queryset = Flat.objects.filter(
            building=building,
            wing=wing,
            flat_number__iexact=flat_number
        )

        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise serializers.ValidationError({
                "flat_number":
                "Flat already exists in this wing."
            })

        return attrs