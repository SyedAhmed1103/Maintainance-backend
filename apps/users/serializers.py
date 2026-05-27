from rest_framework import serializers

from .models import User


# =========================
# REGISTER SERIALIZER
# =========================

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'building_id',
            'user_type',
            'password',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


# =========================
# LOGIN SERIALIZER
# =========================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField()


# =========================
# USER SERIALIZER
# =========================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        exclude = ['password']


# =========================
# UPDATE USER SERIALIZER
# =========================

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'phone',
            'building_id',
            'user_type',
        ]


# =========================
# FORGOT PASSWORD
# =========================

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


# =========================
# RESET PASSWORD
# =========================

class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField()

    password = serializers.CharField()