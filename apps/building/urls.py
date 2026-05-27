from django.urls import path

from .views import (
    BuildingCreateAPIView,
    BuildingListAPIView,
    BuildingDetailAPIView,
    BuildingUpdateAPIView,
    BuildingDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE BUILDING
    # ==================================================

    path(
        'create/',
        BuildingCreateAPIView.as_view(),
        name='building-create'
    ),

    # ==================================================
    # BUILDING LIST
    # ==================================================

    path(
        '',
        BuildingListAPIView.as_view(),
        name='building-list'
    ),

    # ==================================================
    # BUILDING DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        BuildingDetailAPIView.as_view(),
        name='building-detail'
    ),

    # ==================================================
    # UPDATE BUILDING
    # ==================================================

    path(
        'update/<int:pk>/',
        BuildingUpdateAPIView.as_view(),
        name='building-update'
    ),

    # ==================================================
    # DELETE BUILDING
    # ==================================================

    path(
        'delete/<int:pk>/',
        BuildingDeleteAPIView.as_view(),
        name='building-delete'
    ),
]