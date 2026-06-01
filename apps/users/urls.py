from django.urls import path

from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE USER
    # ==================================================

    path(
        'create/',
        UserCreateAPIView.as_view(),
        name='user-create'
    ),

    # ==================================================
    # USER LIST
    # ==================================================

    path(
        '',
        UserListAPIView.as_view(),
        name='user-list'
    ),

    # ==================================================
    # USER DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        UserDetailAPIView.as_view(),
        name='user-detail'
    ),

    # ==================================================
    # UPDATE USER
    # ==================================================

    path(
        'update/<int:pk>/',
        UserUpdateAPIView.as_view(),
        name='user-update'
    ),

    # ==================================================
    # DELETE USER
    # ==================================================

    path(
        'delete/<int:pk>/',
        UserDeleteAPIView.as_view(),
        name='user-delete'
    ),
]