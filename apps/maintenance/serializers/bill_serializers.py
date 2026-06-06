from rest_framework import serializers

from apps.maintenance.models import (
    MaintenanceBill
)


class MaintenanceBillSerializer(
    serializers.ModelSerializer
):

    flat_number = serializers.CharField(
        source='flat.flat_number',
        read_only=True
    )

    class Meta:

        model = MaintenanceBill

        fields = [
            'id',
            'flat',
            'flat_number',
            'bill_type',
            'month',
            'year',
            'amount',
            'paid_amount',
            'pending_amount',
            'due_date',
            'generated_on',
            'status',
            'notes',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'generated_on',
            'created_at',
            'updated_at',
        ]

    def validate_amount(
        self,
        value
    ):

        if value <= 0:

            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value

    def validate_paid_amount(
        self,
        value
    ):

        if value < 0:

            raise serializers.ValidationError(
                "Paid amount cannot be negative."
            )

        return value

    def validate_pending_amount(
        self,
        value
    ):

        if value < 0:

            raise serializers.ValidationError(
                "Pending amount cannot be negative."
            )

        return value