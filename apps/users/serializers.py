from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    full_name = serializers.SerializerMethodField()

    owned_flats = serializers.SerializerMethodField()

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )

    flat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:

        model = User

        fields = [
            'id',

            'first_name',
            'last_name',
            'full_name',

            'email',
            'password',
            'mobile',

            'user_type',

            'building',
            'building_name',

            'flat_ids',
            'owned_flats',

            'is_verified',
            'is_active',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'building_name',
            'full_name',
            'owned_flats',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

    def get_full_name(self, obj):

        return (
            f"{obj.first_name} "
            f"{obj.last_name or ''}"
        ).strip()

    def get_owned_flats(self, obj):

        return [
            {
                "id": flat.id,
                "flat_number": flat.flat_number,
                "wing": flat.wing.wing_name,
                "flat_type": flat.flat_type,
            }
            for flat in obj.flats.select_related(
                'wing'
            )
        ]

    # ==================================================
    # VALIDATIONS
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
                pk=self.instance.pk
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

        if not (10 <= len(value) <= 15):

            raise serializers.ValidationError(
                "Mobile number must be between 10 and 15 digits."
            )

        queryset = User.objects.filter(
            mobile=value
        )

        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Mobile number already exists."
            )

        return value

    def create(self, validated_data):

        validated_data.pop(
            'flat_ids',
            None
        )

        validated_data.pop(
            'password',
            None
        )

        return User.objects.create(
            **validated_data
        )


    def update(
        self,
        instance,
        validated_data
    ):

        validated_data.pop(
            'flat_ids',
            None
        )

        validated_data.pop(
            'password',
            None
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        return instance