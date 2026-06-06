from rest_framework import serializers

from apps.maintenance.models import (
    Payment,
    PaymentAdjustment
)


class PaymentSerializer(
    serializers.ModelSerializer
):

    flat_number = serializers.CharField(
        source='flat.flat_number',
        read_only=True
    )

    class Meta:

        model = Payment

        fields = [
            'id',
            'flat',
            'flat_number',
            'amount',
            'unallocated_amount',
            'receipt_number',
            'payment_mode',
            'transaction_id',
            'remarks',
            'paid_at',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'receipt_number',
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


class PaymentAdjustmentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PaymentAdjustment

        fields = [
            'id',
            'payment',
            'bill',
            'adjusted_amount',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_adjusted_amount(
        self,
        value
    ):

        if value <= 0:

            raise serializers.ValidationError(
                "Adjusted amount must be greater than zero."
            )

        return value
    
class PaymentReceiveRequestSerializer(
    serializers.Serializer
):

    flat_id = serializers.IntegerField()

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_mode = serializers.ChoiceField(
        choices=[
            'online',
            'cash',
            'cheque'
        ]
    )

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    paid_at = serializers.DateTimeField()