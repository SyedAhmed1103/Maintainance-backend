from rest_framework import serializers

from apps.maintenance.models import (
    MaintenanceConfig
)


class MaintenanceConfigSerializer(
    serializers.ModelSerializer
):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = MaintenanceConfig

        fields = [
            'id',
            'building',
            'building_name',
            'calculation_type',
            'fixed_amount',
            'rate_per_sqft',
            'effective_from',
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