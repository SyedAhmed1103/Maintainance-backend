from django.urls import path

from .views import (
    BuildingCreateAPIView,
    BuildingListAPIView,
    BuildingDetailAPIView,
    BuildingUpdateAPIView,
    BuildingDeleteAPIView,
)

urlpatterns = [

    # Create Building
    path(
        '',
        BuildingListAPIView.as_view(),
        name='building-list'
    ),

    path(
        'create/',
        BuildingCreateAPIView.as_view(),
        name='building-create'
    ),

    # Building Detail
    path(
        '<int:pk>/',
        BuildingDetailAPIView.as_view(),
        name='building-detail'
    ),

    # Update Building
    path(
        '<int:pk>/update/',
        BuildingUpdateAPIView.as_view(),
        name='building-update'
    ),

    # Deactivate Building
    path(
        '<int:pk>/delete/',
        BuildingDeleteAPIView.as_view(),
        name='building-delete'
    ),
]