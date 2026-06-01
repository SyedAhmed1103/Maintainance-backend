from django.urls import path

from .views import (
    AdminCreateAPIView,
    AdminListAPIView,
    AdminDetailAPIView,
    AdminUpdateAPIView,
    AdminDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE ADMIN
    # ==================================================

    path(
        'create/',
        AdminCreateAPIView.as_view(),
        name='admin-create'
    ),

    # ==================================================
    # ADMIN LIST
    # ==================================================

    path(
        '',
        AdminListAPIView.as_view(),
        name='admin-list'
    ),

    # ==================================================
    # ADMIN DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        AdminDetailAPIView.as_view(),
        name='admin-detail'
    ),

    # ==================================================
    # UPDATE ADMIN
    # ==================================================

    path(
        'update/<int:pk>/',
        AdminUpdateAPIView.as_view(),
        name='admin-update'
    ),

    # ==================================================
    # DELETE ADMIN
    # ==================================================

    path(
        'delete/<int:pk>/',
        AdminDeleteAPIView.as_view(),
        name='admin-delete'
    ),
]