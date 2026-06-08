from rest_framework import serializers

from .models import Admin


class AdminSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Admin

        fields = [
            'id',
            'building',
            'building_name',
            'name',
            'mobile',
            'email',
            'password',
            'is_active',
            'created_at',
            'updated_at',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

        read_only_fields = [
            'id',
            'building_name',
            'created_at',
            'updated_at',
        ]

    # ==================================================
    # FIELD VALIDATIONS
    # ==================================================

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Name must be at least 3 characters long."
            )

        return value.title()

    def validate_email(self, value):

        value = value.strip().lower()

        queryset = Admin.objects.filter(
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

        return value

    def validate_password(self, value):

        if len(value) < 6:

            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
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

        email = attrs.get(
            'email',
            self.instance.email if self.instance else None
        )

        queryset = Admin.objects.filter(
            building=building,
            email__iexact=email
        )

        if self.instance:

            queryset = queryset.exclude(
                id=self.instance.id
            )

        return attrs
    
class AdminLoginSerializer(serializers.Serializer):

    building = serializers.IntegerField()

    mobile = serializers.CharField(
        max_length=15
    )

    password = serializers.CharField(
        max_length=255,
        write_only=True
    )