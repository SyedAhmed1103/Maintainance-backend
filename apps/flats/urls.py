from django.urls import path

from .views import (
    FlatCreateAPIView,
    FlatListAPIView,
    FlatDetailAPIView,
    FlatUpdateAPIView,
    FlatDeleteAPIView,
)

urlpatterns = [

    # List Flats
    path(
        '',
        FlatListAPIView.as_view(),
        name='flat-list'
    ),

    # Create Flat
    path(
        'create/',
        FlatCreateAPIView.as_view(),
        name='flat-create'
    ),

    # Flat Detail
    path(
        '<int:pk>/',
        FlatDetailAPIView.as_view(),
        name='flat-detail'
    ),

    # Update Flat
    path(
        '<int:pk>/update/',
        FlatUpdateAPIView.as_view(),
        name='flat-update'
    ),

    # Deactivate Flat
    path(
        '<int:pk>/delete/',
        FlatDeleteAPIView.as_view(),
        name='flat-delete'
    ),
]