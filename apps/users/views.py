# =========================================================
# USERS VIEWS.PY
# PART 1
#
# INCLUDED:
# - Imports
# - JWT Helper
# - LoginAPIView
# - ProfileAPIView
# - ChangePasswordAPIView
# - LogoutAPIView
#
# LOGIN SUPPORTS:
# - Building ID
# - Email + Password
# - Mobile + Password
#
# REQUEST:
#
# {
#   "building_id": 1,
#   "username": "admin@gmail.com",
#   "password": "123456"
# }
#
# OR
#
# {
#   "building_id": 1,
#   "username": "9876543210",
#   "password": "123456"
# }
#
# =========================================================

from django.db.models import Q
from django.utils import timezone

from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.generics import (
    GenericAPIView
)

from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from .models import User

from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)


# =========================================================
# JWT TOKEN HELPER
# =========================================================

def get_tokens_for_user(
    user
):

    refresh = (
        RefreshToken.for_user(
            user
        )
    )

    refresh["user_id"] = (
        user.id
    )

    refresh["email"] = (
        user.email
    )

    refresh["mobile"] = (
        user.mobile
    )

    refresh["user_type"] = (
        user.user_type
    )

    refresh["building_id"] = (
        user.building_id
    )

    refresh["flat_id"] = (
        user.flat_id
    )

    return {

        "refresh": str(
            refresh
        ),

        "access": str(
            refresh.access_token
        ),
    }


# =========================================================
# LOGIN
# =========================================================

class LoginAPIView(
    GenericAPIView
):

    serializer_class = (
        LoginSerializer
    )

    authentication_classes = []

    permission_classes = []

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        building_id = (
            serializer.validated_data[
                "building_id"
            ]
        )

        username = (
            serializer.validated_data[
                "username"
            ]
            .strip()
        )

        password = (
            serializer.validated_data[
                "password"
            ]
        )

        try:

            user = (
                User.objects
                .select_related(
                    "building",
                    "flat"
                )
                .get(
                    (
                        Q(
                            email__iexact=username
                        )
                        |
                        Q(
                            mobile=username
                        )
                    ),
                    building_id=building_id,
                    is_active=True,
                    deleted_at__isnull=True
                )
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                    "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(
            password
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.last_login = (
            timezone.now()
        )

        user.save(
            update_fields=[
                "last_login"
            ]
        )

        tokens = (
            get_tokens_for_user(
                user
            )
        )

        return Response(
            {
                "success": True,

                "message":
                "Login successful.",

                "tokens":
                tokens,

                "user":
                ProfileSerializer(
                    user,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PROFILE
# =========================================================

class ProfileAPIView(
    GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = (
        ProfileSerializer
    )

    def get(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                request.user,
                context={
                    "request":
                    request
                }
            )
        )

        return Response(
            {
                "success": True,
                "data":
                serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# CHANGE PASSWORD
# =========================================================

class ChangePasswordAPIView(
    GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = (
        ChangePasswordSerializer
    )

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        old_password = (
            serializer.validated_data[
                "old_password"
            ]
        )

        new_password = (
            serializer.validated_data[
                "new_password"
            ]
        )

        if not user.check_password(
            old_password
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Old password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(
            new_password
        )

        user.save(
            update_fields=[
                "password"
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# LOGOUT
# =========================================================

class LogoutAPIView(
    GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        refresh_token = (
            request.data.get(
                "refresh"
            )
        )

        if not refresh_token:

            return Response(
                {
                    "success": False,
                    "message":
                    "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            token = (
                RefreshToken(
                    refresh_token
                )
            )

            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message":
                    "Logout successful."
                },
                status=status.HTTP_200_OK
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message":
                    "Invalid refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

# =========================================================
#
# INCLUDED:
# - UserCreateAPIView
# - UserListAPIView
# - UserDetailAPIView
#
#
# AVATAR LOGIC INCLUDED
# USING MediaService
#
# ONLY ADMIN CAN:
# - Create User
# - List Users
# - View User Details
#
# =========================================================

from django.db import transaction
from django.db.models import Q

from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from .models import User

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
)

from apps.media_manager.models import (
    Media
)

from apps.media_manager.services import (
    MediaService
)


# =========================================================
# CREATE USER
# =========================================================

class UserCreateAPIView(
    CreateAPIView
):

    queryset = (
        User.objects.all()
    )

    serializer_class = (
        UserCreateSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.user_type
            != User.UserType.ADMIN
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        password = (
            validated_data.pop(
                "password"
            )
        )

        validated_data.pop("user_type", None)

        user = User.objects.create(
            user_type=User.UserType.OWNER,
            **validated_data
)

        user.set_password(
            password
        )

        user.save()

        avatar = (
            request.FILES.get(
                "avatar"
            )
        )

        if avatar:

            MediaService.upload_single(
                instance=user,
                file=avatar,
                category=Media.Category.AVATAR,
                media_type=Media.MediaType.IMAGE
            )

        return Response(
            {
                "success": True,

                "message":
                "User created successfully.",

                "data":
                UserSerializer(
                    user,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# USER LIST
# =========================================================

class UserListAPIView(
    ListAPIView
):

    serializer_class = (
        UserSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(
        self
    ):

        queryset = (
            User.objects
            .select_related(
                "building",
                "flat"
            )
            .filter(
                deleted_at__isnull=True
            )
            .order_by(
                "-created_at"
            )
        )

        search = (
            self.request.GET.get(
                "search"
            )
        )

        building_id = (
            self.request.GET.get(
                "building_id"
            )
        )

        flat_id = (
            self.request.GET.get(
                "flat_id"
            )
        )

        user_type = (
            self.request.GET.get(
                "user_type"
            )
        )

        is_active = (
            self.request.GET.get(
                "is_active"
            )
        )

        if search:

            queryset = (
                queryset.filter(
                    Q(
                        first_name__icontains=search
                    )
                    |
                    Q(
                        last_name__icontains=search
                    )
                    |
                    Q(
                        email__icontains=search
                    )
                    |
                    Q(
                        mobile__icontains=search
                    )
                )
            )

        if building_id:

            queryset = (
                queryset.filter(
                    building_id=building_id
                )
            )

        if flat_id:

            queryset = (
                queryset.filter(
                    flat_id=flat_id
                )
            )

        if user_type:

            queryset = (
                queryset.filter(
                    user_type=user_type
                )
            )

        if is_active:

            if (
                is_active.lower()
                == "true"
            ):
                queryset = (
                    queryset.filter(
                        is_active=True
                    )
                )

            elif (
                is_active.lower()
                == "false"
            ):
                queryset = (
                    queryset.filter(
                        is_active=False
                    )
                )

        return queryset

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = (
            self.get_queryset()
        )

        serializer = (
            self.get_serializer(
                queryset,
                many=True,
                context={
                    "request":
                    request
                }
            )
        )

        return Response(
            {
                "success": True,

                "count":
                queryset.count(),

                "data":
                serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# USER DETAIL
# =========================================================

class UserDetailAPIView(
    RetrieveAPIView
):

    queryset = (
        User.objects
        .select_related(
            "building",
            "flat"
        )
        .filter(
            deleted_at__isnull=True
        )
    )

    serializer_class = (
        UserSerializer
    )

    lookup_field = "pk"

    permission_classes = [
        IsAuthenticated
    ]

    def retrieve(
        self,
        request,
        *args,
        **kwargs
    ):

        user = (
            self.get_object()
        )

        serializer = (
            self.get_serializer(
                user,
                context={
                    "request":
                    request
                }
            )
        )

        return Response(
            {
                "success": True,

                "data":
                serializer.data
            },
            status=status.HTTP_200_OK
        )
    
# =========================================================
# USERS VIEWS.PY
# PART 3
#
# INCLUDED:
# - UserUpdateAPIView
# - UserDeleteAPIView (SOFT DELETE)
# - ProfileUpdateAPIView
# - Avatar Replace Logic
#
# PASTE BELOW PART 2
#
# =========================================================

from django.db import transaction
from django.utils import timezone

from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.generics import (
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
)

from .models import User

from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ProfileSerializer,
)

from apps.media_manager.models import (
    Media
)

from apps.media_manager.services import (
    MediaService
)


# =========================================================
# UPDATE USER
# =========================================================

class UserUpdateAPIView(
    UpdateAPIView
):

    queryset = (
        User.objects.filter(
            deleted_at__isnull=True
        )
    )

    serializer_class = (
        UserUpdateSerializer
    )

    lookup_field = "pk"

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.user_type
            != User.UserType.ADMIN
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = (
            self.get_object()
        )

        serializer = (
            self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        password = (
            validated_data.pop(
                "password",
                None
            )
        )

        for field, value in (
            validated_data.items()
        ):

            setattr(
                instance,
                field,
                value
            )

        if password:

            instance.set_password(
                password
            )

        instance.save()

        avatar = (
            request.FILES.get(
                "avatar"
            )
        )

        if avatar:

            MediaService.replace_single(
                instance=instance,
                file=avatar,
                category=Media.Category.AVATAR,
                media_type=Media.MediaType.IMAGE
            )

        return Response(
            {
                "success": True,

                "message":
                "User updated successfully.",

                "data":
                UserSerializer(
                    instance,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_200_OK
        )

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# PROFILE UPDATE
# =========================================================

class ProfileUpdateAPIView(
    GenericAPIView
):

    serializer_class = (
        UserUpdateSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def put(
        self,
        request,
        *args,
        **kwargs
    ):

        user = request.user

        serializer = (
            self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        avatar = (
            request.FILES.get(
                "avatar"
            )
        )

        if avatar:

            MediaService.replace_single(
                instance=user,
                file=avatar,
                category=Media.Category.AVATAR,
                media_type=Media.MediaType.IMAGE
            )

        return Response(
            {
                "success": True,

                "message":
                "Profile updated successfully.",

                "data":
                ProfileSerializer(
                    user,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# DELETE USER (SOFT DELETE)
# =========================================================

class UserDeleteAPIView(
    DestroyAPIView
):

    queryset = (
        User.objects.filter(
            deleted_at__isnull=True
        )
    )

    serializer_class = (
        UserSerializer
    )

    lookup_field = "pk"

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.user_type
            != User.UserType.ADMIN
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user = (
            self.get_object()
        )

        user.deleted_at = (
            timezone.now()
        )

        user.is_active = False

        user.save(
            update_fields=[
                "deleted_at",
                "is_active"
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "User deleted successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# REMOVE AVATAR
# =========================================================

class RemoveAvatarAPIView(
    GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        MediaService.delete_single_by_category(
            instance=request.user,
            category=Media.Category.AVATAR
        )

        return Response(
            {
                "success": True,
                "message":
                "Avatar removed successfully."
            },
            status=status.HTTP_200_OK
        )
    
# =========================================================
# USERS VIEWS.PY
# PART 3
#
# INCLUDED:
# - UserUpdateAPIView
# - UserDeleteAPIView (SOFT DELETE)
# - ProfileUpdateAPIView
# - Avatar Replace Logic
#
# PASTE BELOW PART 2
#
# =========================================================

from django.db import transaction
from django.utils import timezone

from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.generics import (
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
)

from .models import User

from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ProfileSerializer,
)

from apps.media_manager.models import (
    Media
)

from apps.media_manager.services import (
    MediaService
)


# =========================================================
# UPDATE USER
# =========================================================

class UserUpdateAPIView(
    UpdateAPIView
):

    queryset = (
        User.objects.filter(
            deleted_at__isnull=True
        )
    )

    serializer_class = (
        UserUpdateSerializer
    )

    lookup_field = "pk"

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.user_type
            != User.UserType.ADMIN
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = (
            self.get_object()
        )

        serializer = (
            self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        password = (
            validated_data.pop(
                "password",
                None
            )
        )

        for field, value in (
            validated_data.items()
        ):

            setattr(
                instance,
                field,
                value
            )

        if password:

            instance.set_password(
                password
            )

        instance.save()

        avatar = (
            request.FILES.get(
                "avatar"
            )
        )

        if avatar:

            MediaService.replace_single(
                instance=instance,
                file=avatar,
                category=Media.Category.AVATAR,
                media_type=Media.MediaType.IMAGE
            )

        return Response(
            {
                "success": True,

                "message":
                "User updated successfully.",

                "data":
                UserSerializer(
                    instance,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_200_OK
        )

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# PROFILE UPDATE
# =========================================================

class ProfileUpdateAPIView(
    GenericAPIView
):

    serializer_class = (
        UserUpdateSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def put(
        self,
        request,
        *args,
        **kwargs
    ):

        user = request.user

        serializer = (
            self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        avatar = (
            request.FILES.get(
                "avatar"
            )
        )

        if avatar:

            MediaService.replace_single(
                instance=user,
                file=avatar,
                category=Media.Category.AVATAR,
                media_type=Media.MediaType.IMAGE
            )

        return Response(
            {
                "success": True,

                "message":
                "Profile updated successfully.",

                "data":
                ProfileSerializer(
                    user,
                    context={
                        "request":
                        request
                    }
                ).data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# DELETE USER (SOFT DELETE)
# =========================================================

class UserDeleteAPIView(
    DestroyAPIView
):

    queryset = (
        User.objects.filter(
            deleted_at__isnull=True
        )
    )

    serializer_class = (
        UserSerializer
    )

    lookup_field = "pk"

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.user_type
            != User.UserType.ADMIN
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user = (
            self.get_object()
        )

        user.deleted_at = (
            timezone.now()
        )

        user.is_active = False

        user.save(
            update_fields=[
                "deleted_at",
                "is_active"
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "User deleted successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# REMOVE AVATAR
# =========================================================

class RemoveAvatarAPIView(
    GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        MediaService.delete_single_by_category(
            instance=request.user,
            category=Media.Category.AVATAR
        )

        return Response(
            {
                "success": True,
                "message":
                "Avatar removed successfully."
            },
            status=status.HTTP_200_OK
        )
    

# =========================================================
# USERS VIEWS.PY
# PART 4
#
# INCLUDED:
# - ForgotPasswordAPIView
# - ResetPasswordAPIView
# - AdminOnlyPermission
# - Complete URLs
#
# PASTE BELOW PART 3
# =========================================================

from django.conf import settings

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)

from django.utils.encoding import (
    force_bytes,
    force_str
)

from django.contrib.auth.tokens import (
    default_token_generator
)

from django.core.mail import send_mail

from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated
)

from rest_framework.generics import (
    GenericAPIView
)

from .models import User

from .serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


# =========================================================
# ADMIN ONLY PERMISSION
# =========================================================

class IsAdminUserType(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_type
            == User.UserType.ADMIN
        )


# =========================================================
# FORGOT PASSWORD
# =========================================================

class ForgotPasswordAPIView(
    GenericAPIView
):

    serializer_class = (
        ForgotPasswordSerializer
    )

    authentication_classes = []
    permission_classes = []

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = (
            serializer.validated_data[
                "email"
            ]
            .lower()
            .strip()
        )

        try:

            user = (
                User.objects.get(
                    email=email,
                    deleted_at__isnull=True
                )
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": True,
                    "message":
                    "If an account exists, a password reset link has been sent."
                },
                status=status.HTTP_200_OK
            )

        uid = (
            urlsafe_base64_encode(
                force_bytes(
                    user.pk
                )
            )
        )

        token = (
            default_token_generator.make_token(
                user
            )
        )

        frontend_url = (
            getattr(
                settings,
                "FRONTEND_URL",
                "http://localhost:4200"
            )
        )

        reset_link = (
            f"{frontend_url}"
            f"/reset-password"
            f"?uid={uid}"
            f"&token={token}"
        )

        subject = (
            "Reset Your Password"
        )

        message = f"""
Hello {user.full_name},

We received a request to reset your password.

Click the link below:

{reset_link}

If you did not request this password reset,
please ignore this email.

Thank You.
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

        return Response(
            {
                "success": True,
                "message":
                "Password reset email sent successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# RESET PASSWORD
# =========================================================

class ResetPasswordAPIView(
    GenericAPIView
):

    serializer_class = (
        ResetPasswordSerializer
    )

    authentication_classes = []
    permission_classes = []

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        uid = (
            request.data.get(
                "uid"
            )
        )

        token = (
            request.data.get(
                "token"
            )
        )

        password = (
            serializer.validated_data[
                "password"
            ]
        )

        try:

            user_id = (
                force_str(
                    urlsafe_base64_decode(
                        uid
                    )
                )
            )

            user = (
                User.objects.get(
                    pk=user_id
                )
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message":
                    "Invalid reset link."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (
            default_token_generator.check_token(
                user,
                token
            )
        ):

            return Response(
                {
                    "success": False,
                    "message":
                    "Reset link expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(
            password
        )

        user.save(
            update_fields=[
                "password"
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "Password reset successful."
            },
            status=status.HTTP_200_OK
        )