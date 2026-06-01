from datetime import date

from rest_framework import serializers

from .models import Maintenance


class MaintenanceSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Maintenance

        fields = [
            'id',
            'building',
            'building_name',
            'title',
            'generated_date',
            'month',
            'year',
            'due_date',
            'status',
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

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )

        return value.title()

    def validate_month(self, value):

        if value < 1 or value > 12:

            raise serializers.ValidationError(
                "Month must be between 1 and 12."
            )

        return value

    def validate_year(self, value):

        if value < 2020:

            raise serializers.ValidationError(
                "Invalid year."
            )

        return value

    def validate_due_date(self, value):

        if value < date.today():

            raise serializers.ValidationError(
                "Due date cannot be in the past."
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

        month = attrs.get(
            'month',
            self.instance.month if self.instance else None
        )

        year = attrs.get(
            'year',
            self.instance.year if self.instance else None
        )

        generated_date = attrs.get(
            'generated_date',
            self.instance.generated_date if self.instance else None
        )

        due_date = attrs.get(
            'due_date',
            self.instance.due_date if self.instance else None
        )

        queryset = Maintenance.objects.filter(
            building=building,
            month=month,
            year=year
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError({
                "month":
                "Maintenance already exists for this month and year."
            })

        if generated_date and due_date:

            if due_date < generated_date:

                raise serializers.ValidationError({
                    "due_date":
                    "Due date cannot be before generated date."
                })

        return attrs