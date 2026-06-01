from django.urls import path

from .views import (
    MaintenanceDetailCreateAPIView,
    MaintenanceDetailListAPIView,
    MaintenanceDetailAPIView,
    MaintenanceDetailUpdateAPIView,
    MaintenanceDetailDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE MAINTENANCE DETAIL
    # ==================================================

    path(
        'create/',
        MaintenanceDetailCreateAPIView.as_view(),
        name='maintenance-detail-create'
    ),

    # ==================================================
    # MAINTENANCE DETAIL LIST
    # ==================================================

    path(
        '',
        MaintenanceDetailListAPIView.as_view(),
        name='maintenance-detail-list'
    ),

    # ==================================================
    # MAINTENANCE DETAIL DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        MaintenanceDetailAPIView.as_view(),
        name='maintenance-detail-detail'
    ),

    # ==================================================
    # UPDATE MAINTENANCE DETAIL
    # ==================================================

    path(
        'update/<int:pk>/',
        MaintenanceDetailUpdateAPIView.as_view(),
        name='maintenance-detail-update'
    ),

    # ==================================================
    # DELETE MAINTENANCE DETAIL
    # ==================================================

    path(
        'delete/<int:pk>/',
        MaintenanceDetailDeleteAPIView.as_view(),
        name='maintenance-detail-delete'
    ),
]