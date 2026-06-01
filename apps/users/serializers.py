from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    flat_number = serializers.SerializerMethodField()

    full_name = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'mobile',
            'user_type',
            'building',
            'building_name',
            'flat',
            'flat_number',
            'is_verified',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'building_name',
            'flat_number',
            'full_name',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_full_name(self, obj):

        return f"{obj.first_name} {obj.last_name or ''}".strip()

    def get_flat_number(self, obj):

        if obj.flat:

            return f"{obj.flat.wing}-{obj.flat.flat_number}"

        return None

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_first_name(self, value):

        value = value.strip()

        if len(value) < 2:

            raise serializers.ValidationError(
                "First name must be at least 2 characters long."
            )

        return value.title()

    def validate_last_name(self, value):

        if not value:
            return value

        return value.strip().title()

    def validate_email(self, value):

        value = value.strip().lower()

        queryset = User.objects.filter(
            email__iexact=value
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_mobile(self, value):

        value = value.strip()

        if not value.isdigit():

            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) < 10 or len(value) > 15:

            raise serializers.ValidationError(
                "Mobile number must be between 10 and 15 digits."
            )

        queryset = User.objects.filter(
            mobile=value
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Mobile number already exists."
            )

        return value

    # ==================================================
    # OBJECT LEVEL VALIDATION
    # ==================================================

    def validate(self, attrs):

        user_type = attrs.get(
            'user_type',
            self.instance.user_type if self.instance else None
        )

        building = attrs.get(
            'building',
            self.instance.building if self.instance else None
        )

        flat = attrs.get(
            'flat',
            self.instance.flat if self.instance else None
        )

        if user_type in ['owner', 'tenant']:

            if not building:

                raise serializers.ValidationError({
                    "building":
                    "Building is required."
                })

            if not flat:

                raise serializers.ValidationError({
                    "flat":
                    "Flat is required."
                })

        if flat and building:

            if flat.building_id != building.id:

                raise serializers.ValidationError({
                    "flat":
                    "Selected flat does not belong to the selected building."
                })

        return attrs