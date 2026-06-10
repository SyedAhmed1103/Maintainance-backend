from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import User
from apps.media_manager.models import Media


# =========================================================
# AVATAR MIXIN
# =========================================================

class AvatarMixin:

    def get_avatar(self, obj):

        try:

            content_type = (
                ContentType.objects.get_for_model(
                    User
                )
            )

            media = (
                Media.objects.filter(
                    content_type=content_type,
                    object_id=obj.id,
                    category=Media.Category.AVATAR,
                    is_active=True
                )
                .first()
            )

            if not media:
                return None

            request = self.context.get(
                "request"
            )

            if request and media.file:

                return (
                    request.build_absolute_uri(
                        media.file.url
                    )
                )

            return media.file_url

        except Exception:
            return None


# =========================================================
# USER LIST / DETAIL
# =========================================================

class UserSerializer(
    AvatarMixin,
    serializers.ModelSerializer
):

    full_name = serializers.ReadOnlyField()

    building_name = serializers.CharField(
        source="building.building_name",
        read_only=True
    )

    flat_number = serializers.CharField(
        source="flat.flat_number",
        read_only=True
    )

    avatar = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [

            "id",

            "first_name",
            "last_name",
            "full_name",

            "email",
            "mobile",

            "user_type",

            "building",
            "building_name",

            "flat",
            "flat_number",

            "avatar",

            "is_verified",
            "verified_at",

            "is_active",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "verified_at",
        ]


# =========================================================
# USER CREATE
# =========================================================

class UserCreateSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:

        model = User

        fields = [

            "first_name",
            "last_name",

            "email",
            "mobile",

            "password",

            "user_type",

            "building",
            "flat",

            "is_verified",
            "is_active",
        ]


# =========================================================
# USER UPDATE
# =========================================================

class UserUpdateSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:

        model = User

        fields = [

            "first_name",
            "last_name",

            "email",
            "mobile",

            "password",

            "user_type",

            "building",
            "flat",

            "is_verified",
            "is_active",
        ]


# =========================================================
# LOGIN
# =========================================================

class LoginSerializer(
    serializers.Serializer
):

    building_id = serializers.IntegerField()

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )


# =========================================================
# PROFILE
# =========================================================

class ProfileSerializer(
    AvatarMixin,
    serializers.ModelSerializer
):

    full_name = serializers.ReadOnlyField()

    avatar = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [

            "id",

            "first_name",
            "last_name",
            "full_name",

            "email",
            "mobile",

            "user_type",

            "building",
            "flat",

            "avatar",

            "is_verified",
            "verified_at",
        ]


# =========================================================
# CHANGE PASSWORD
# =========================================================

class ChangePasswordSerializer(
    serializers.Serializer
):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=6
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

class ForgotPasswordSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()


# =========================================================
# RESET PASSWORD
# =========================================================

class ResetPasswordSerializer(
    serializers.Serializer
):

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )


# =========================================================
# USER DROPDOWN
# =========================================================

class UserDropdownSerializer(
    serializers.ModelSerializer
):

    full_name = serializers.ReadOnlyField()

    class Meta:

        model = User

        fields = [
            "id",
            "full_name",
            "user_type",
        ]