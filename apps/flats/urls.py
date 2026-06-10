from django.urls import path

from .views import (
    FlatCreateAPIView,
    FlatListAPIView,
    FlatByBuildingAPIView,
    FlatDetailAPIView,
    FlatUpdateAPIView,
    FlatDeleteAPIView,

    FlatTypeCreateAPIView,
    FlatTypeListAPIView,
    FlatTypeByBuildingAPIView,
    FlatTypeDetailAPIView,
    FlatTypeUpdateAPIView,
    FlatTypeDeleteAPIView,
)

urlpatterns = [

    # =====================================================
    # FLAT TYPE
    # =====================================================

    path(
        'flat-types/create/',
        FlatTypeCreateAPIView.as_view(),
        name='flat-type-create'
    ),

    path(
        'flat-types/',
        FlatTypeListAPIView.as_view(),
        name='flat-type-list'
    ),

    path(
        'flat-types/building/<int:building_id>/',
        FlatTypeByBuildingAPIView.as_view(),
        name='flat-type-by-building'
    ),

    path(
        'flat-types/<int:pk>/',
        FlatTypeDetailAPIView.as_view(),
        name='flat-type-detail'
    ),

    path(
        'flat-types/<int:pk>/update/',
        FlatTypeUpdateAPIView.as_view(),
        name='flat-type-update'
    ),

    path(
        'flat-types/<int:pk>/delete/',
        FlatTypeDeleteAPIView.as_view(),
        name='flat-type-delete'
    ),

    # =====================================================
    # FLATS
    # =====================================================

    path(
        'create/',
        FlatCreateAPIView.as_view(),
        name='flat-create'
    ),

    # path(
    #     '',
    #     FlatListAPIView.as_view(),
    #     name='flat-list'
    # ),

    path(
        'building/<int:building_id>/',
        FlatByBuildingAPIView.as_view(),
        name='flat-by-building'
    ),

    path(
        '<int:pk>/',
        FlatDetailAPIView.as_view(),
        name='flat-detail'
    ),

    path(
        '<int:pk>/update/',
        FlatUpdateAPIView.as_view(),
        name='flat-update'
    ),

    path(
        '<int:pk>/delete/',
        FlatDeleteAPIView.as_view(),
        name='flat-delete'
    ),
]
