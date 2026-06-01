from django.urls import path

from .views import (
    MaintenanceCreateAPIView,
    MaintenanceListAPIView,
    MaintenanceDetailAPIView,
    MaintenanceUpdateAPIView,
    MaintenanceDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE MAINTENANCE
    # ==================================================

    path(
        'create/',
        MaintenanceCreateAPIView.as_view(),
        name='maintenance-create'
    ),

    # ==================================================
    # MAINTENANCE LIST
    # ==================================================

    path(
        '',
        MaintenanceListAPIView.as_view(),
        name='maintenance-list'
    ),

    # ==================================================
    # MAINTENANCE DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        MaintenanceDetailAPIView.as_view(),
        name='maintenance-detail'
    ),

    # ==================================================
    # UPDATE MAINTENANCE
    # ==================================================

    path(
        'update/<int:pk>/',
        MaintenanceUpdateAPIView.as_view(),
        name='maintenance-update'
    ),

    # ==================================================
    # DELETE MAINTENANCE
    # ==================================================

    path(
        'delete/<int:pk>/',
        MaintenanceDeleteAPIView.as_view(),
        name='maintenance-delete'
    ),
]