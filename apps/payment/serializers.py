from decimal import Decimal

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    flat_number = serializers.SerializerMethodField()

    receipt_number = serializers.CharField(
        required=False
    )

    class Meta:

        model = Payment

        fields = [
            'id',
            'maintenance_detail',
            'user',
            'user_name',
            'flat',
            'flat_number',
            'amount',
            'receipt_number',
            'payment_mode',
            'transaction_id',
            'payment_date',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_user_name(self, obj):

        return (
            f"{obj.user.first_name} "
            f"{obj.user.last_name or ''}"
        ).strip()

    def get_flat_number(self, obj):

        return (
            f"{obj.flat.wing}-"
            f"{obj.flat.flat_number}"
        )

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_amount(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value

    def validate_receipt_number(self, value):

        value = value.strip().upper()

        queryset = Payment.objects.filter(
            receipt_number__iexact=value
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Receipt number already exists."
            )

        return value

    def validate_transaction_id(self, value):

        if value:

            return value.strip().upper()

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        maintenance_detail = attrs.get(
            'maintenance_detail',
            self.instance.maintenance_detail
            if self.instance else None
        )

        user = attrs.get(
            'user',
            self.instance.user
            if self.instance else None
        )

        flat = attrs.get(
            'flat',
            self.instance.flat
            if self.instance else None
        )

        amount = attrs.get(
            'amount',
            self.instance.amount
            if self.instance else Decimal('0')
        )

        if user and flat:

            if user.flat_id != flat.id:

                raise serializers.ValidationError({
                    "flat":
                    "Selected flat does not belong to user."
                })

        if maintenance_detail and flat:

            if maintenance_detail.flat_id != flat.id:

                raise serializers.ValidationError({
                    "flat":
                    "Selected flat does not belong to maintenance detail."
                })

        if maintenance_detail:

            pending_amount = (
                maintenance_detail.total_amount
            )

            if amount > pending_amount:

                raise serializers.ValidationError({
                    "amount":
                    "Payment amount cannot exceed maintenance amount."
                })

        return attrs