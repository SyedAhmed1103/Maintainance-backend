from datetime import date

from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Expense

        fields = [
            'id',
            'building',
            'building_name',
            'expense_type',
            'amount',
            'description',
            'expense_date',
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

    def validate_expense_type(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Expense type must be at least 3 characters long."
            )

        return value.title()

    def validate_amount(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value

    def validate_description(self, value):

        if value:

            return value.strip()

        return value

    def validate_expense_date(self, value):

        if value > date.today():

            raise serializers.ValidationError(
                "Expense date cannot be in the future."
            )

        return value