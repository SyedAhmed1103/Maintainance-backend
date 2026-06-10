from rest_framework import serializers

from .models import Income


class IncomeSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source="building.name",
        read_only=True
    )

    class Meta:
        model = Income

        fields = [
            "id",
            "building",
            "building_name",
            "income_type",
            "amount",
            "description",
            "reference_number",
            "income_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "building_name",
            "created_at",
            "updated_at",
        )

    def validate_income_type(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Income type is required."
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

        income_date = attrs.get("income_date")

        if income_date is None:
            raise serializers.ValidationError(
                {
                    "income_date":
                    "Income date is required."
                }
            )

        return attrs