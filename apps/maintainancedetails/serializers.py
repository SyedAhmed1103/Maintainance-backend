from decimal import Decimal

from rest_framework import serializers

from .models import MaintenanceDetail


class MaintenanceDetailSerializer(serializers.ModelSerializer):

    flat_number = serializers.SerializerMethodField()

    building_name = serializers.CharField(
        source='flat.building.building_name',
        read_only=True
    )

    maintenance_title = serializers.CharField(
        source='maintenance.title',
        read_only=True
    )

    class Meta:

        model = MaintenanceDetail

        fields = [
            'id',
            'maintenance',
            'maintenance_title',
            'flat',
            'flat_number',
            'building_name',
            'amount',
            'late_fee',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'maintenance_title',
            'flat_number',
            'building_name',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_flat_number(self, obj):

        return f"{obj.flat.wing}-{obj.flat.flat_number}"

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_amount(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Amount cannot be negative."
            )

        return value

    def validate_late_fee(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Late fee cannot be negative."
            )

        return value

    def validate_total_amount(self, value):

        if value < 0:

            raise serializers.ValidationError(
                "Total amount cannot be negative."
            )

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        maintenance = attrs.get(
            'maintenance',
            self.instance.maintenance if self.instance else None
        )

        flat = attrs.get(
            'flat',
            self.instance.flat if self.instance else None
        )

        amount = attrs.get(
            'amount',
            self.instance.amount if self.instance else Decimal('0')
        )

        late_fee = attrs.get(
            'late_fee',
            self.instance.late_fee if self.instance else Decimal('0')
        )

        total_amount = attrs.get(
            'total_amount',
            self.instance.total_amount if self.instance else Decimal('0')
        )

        queryset = MaintenanceDetail.objects.filter(
            maintenance=maintenance,
            flat=flat
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError({
                "flat":
                "Maintenance already generated for this flat."
            })

        expected_total = amount + late_fee

        if total_amount != expected_total:

            raise serializers.ValidationError({
                "total_amount":
                f"Total amount must be {expected_total}."
            })

        if (
            maintenance and
            flat and
            maintenance.building_id != flat.building_id
        ):

            raise serializers.ValidationError({
                "flat":
                "Selected flat does not belong to maintenance building."
            })

        return attrs