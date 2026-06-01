from rest_framework import serializers

from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    flat_number = serializers.SerializerMethodField()

    user_name = serializers.SerializerMethodField()

    class Meta:

        model = Complaint

        fields = [
            'id',
            'building',
            'building_name',
            'flat',
            'flat_number',
            'user',
            'user_name',
            'title',
            'description',
            'admin_remark',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'building_name',
            'flat_number',
            'user_name',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_flat_number(self, obj):

        return (
            f"{obj.flat.wing}-"
            f"{obj.flat.flat_number}"
        )

    def get_user_name(self, obj):

        return (
            f"{obj.user.first_name} "
            f"{obj.user.last_name or ''}"
        ).strip()

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
                "Description must be at least 10 characters long."
            )

        return value

    def validate_admin_remark(self, value):

        if value:

            return value.strip()

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        building = attrs.get(
            'building',
            self.instance.building
            if self.instance else None
        )

        flat = attrs.get(
            'flat',
            self.instance.flat
            if self.instance else None
        )

        user = attrs.get(
            'user',
            self.instance.user
            if self.instance else None
        )

        if flat and building:

            if flat.building_id != building.id:

                raise serializers.ValidationError({
                    "flat":
                    "Selected flat does not belong to selected building."
                })

        if user and building:

            if user.building_id != building.id:

                raise serializers.ValidationError({
                    "user":
                    "Selected user does not belong to selected building."
                })

        if user and flat:

            if user.flat_id != flat.id:

                raise serializers.ValidationError({
                    "user":
                    "Selected user does not belong to selected flat."
                })

        return attrs