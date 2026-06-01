from datetime import date

from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Notice

        fields = [
            'id',
            'building',
            'building_name',
            'title',
            'description',
            'start_date',
            'end_date',
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

    def validate_description(self, value):

        value = value.strip()

        if len(value) < 10:

            raise serializers.ValidationError(
                "Description is too short."
            )

        return value

    def validate_start_date(self, value):

        if value < date.today():

            raise serializers.ValidationError(
                "Start date cannot be in the past."
            )

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        start_date = attrs.get(
            'start_date',
            self.instance.start_date
            if self.instance else None
        )

        end_date = attrs.get(
            'end_date',
            self.instance.end_date
            if self.instance else None
        )

        if start_date and end_date:

            if end_date < start_date:

                raise serializers.ValidationError({
                    "end_date":
                    "End date must be greater than start date."
                })

        return attrs