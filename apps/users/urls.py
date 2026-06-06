from django.urls import path

from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
)

urlpatterns = [

    # List Users
    path(
        '',
        UserListAPIView.as_view(),
        name='user-list'
    ),

    # Create User
    path(
        'create/',
        UserCreateAPIView.as_view(),
        name='user-create'
    ),

    # User Detail
    path(
        '<int:pk>/',
        UserDetailAPIView.as_view(),
        name='user-detail'
    ),

    # Update User
    path(
        '<int:pk>/update/',
        UserUpdateAPIView.as_view(),
        name='user-update'
    ),

    # Deactivate User
    path(
        '<int:pk>/delete/',
        UserDeleteAPIView.as_view(),
        name='user-delete'
    ),
]