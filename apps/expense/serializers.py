from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source="building.name",
        read_only=True
    )

    class Meta:
        model = Expense

        fields = [
            "id",
            "building",
            "building_name",
            "expense_type",
            "amount",
            "description",
            "reference_number",
            "expense_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "building_name",
            "created_at",
            "updated_at",
        )

    def validate_expense_type(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Expense type is required."
            )

        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value

    def validate_reference_number(self, value):
        return value.strip() if value else value

    def validate(self, attrs):

        expense_date = attrs.get("expense_date")

        if expense_date is None:
            raise serializers.ValidationError(
                {
                    "expense_date":
                    "Expense date is required."
                }
            )

        return attrs