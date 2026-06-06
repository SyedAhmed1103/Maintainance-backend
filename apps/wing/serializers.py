from rest_framework import serializers

from .models import Wing


class WingSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(
        source='building.building_name',
        read_only=True
    )

    class Meta:

        model = Wing

        fields = [
            'id',
            'building',
            'building_name',
            'wing_name',
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

    # ==========================================
    # FIELD VALIDATIONS
    # ==========================================

    def validate_wing_name(self, value):

        value = value.strip().upper()

        if len(value) < 1:
            raise serializers.ValidationError(
                "Wing name is required."
            )

        return value

    # ==========================================
    # OBJECT VALIDATION
    # ==========================================

    def validate(self, attrs):

        building = attrs.get(
            'building',
            self.instance.building if self.instance else None
        )

        wing_name = attrs.get(
            'wing_name',
            self.instance.wing_name if self.instance else None
        )

        queryset = Wing.objects.filter(
            building=building,
            wing_name__iexact=wing_name
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError({
                "wing_name":
                "This wing already exists in the selected building."
            })

        return attrs