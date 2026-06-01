from django.urls import path

from .views import (
    FlatCreateAPIView,
    FlatListAPIView,
    FlatDetailAPIView,
    FlatUpdateAPIView,
    FlatDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE FLAT
    # ==================================================

    path(
        'create/',
        FlatCreateAPIView.as_view(),
        name='flat-create'
    ),

    # ==================================================
    # FLAT LIST
    # ==================================================

    path(
        '',
        FlatListAPIView.as_view(),
        name='flat-list'
    ),

    # ==================================================
    # FLAT DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        FlatDetailAPIView.as_view(),
        name='flat-detail'
    ),

    # ==================================================
    # UPDATE FLAT
    # ==================================================

    path(
        'update/<int:pk>/',
        FlatUpdateAPIView.as_view(),
        name='flat-update'
    ),

    # ==================================================
    # DELETE FLAT
    # ==================================================

    path(
        'delete/<int:pk>/',
        FlatDeleteAPIView.as_view(),
        name='flat-delete'
    ),
]