from django.urls import path

from .views import (
    LoginAPIView,
    LogoutAPIView,

    ProfileAPIView,
    ProfileUpdateAPIView,

    ChangePasswordAPIView,

    ForgotPasswordAPIView,
    ResetPasswordAPIView,

    RemoveAvatarAPIView,

    UserCreateAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
)

urlpatterns = [

    # =====================================================
    # AUTH
    # =====================================================

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout"
    ),

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile"
    ),

    path(
        "profile/update/",
        ProfileUpdateAPIView.as_view(),
        name="profile_update"
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password"
    ),

    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot_password"
    ),

    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password"
    ),

    path(
        "profile/avatar/remove/",
        RemoveAvatarAPIView.as_view(),
        name="remove_avatar"
    ),

    # =====================================================
    # USERS CRUD
    # =====================================================

    path(
        "",
        UserListAPIView.as_view(),
        name="user_list"
    ),

    path(
        "create/",
        UserCreateAPIView.as_view(),
        name="user_create"
    ),

    path(
        "<int:pk>/",
        UserDetailAPIView.as_view(),
        name="user_detail"
    ),

    path(
        "<int:pk>/update/",
        UserUpdateAPIView.as_view(),
        name="user_update"
    ),

    path(
        "<int:pk>/delete/",
        UserDeleteAPIView.as_view(),
        name="user_delete"
    ),
]