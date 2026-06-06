from django.urls import path

from .views import (
    WingCreateAPIView,
    WingListAPIView,
    WingDetailAPIView,
    WingUpdateAPIView,
    WingDeleteAPIView,
)

urlpatterns = [

    # List Wings
    path(
        '',
        WingListAPIView.as_view(),
        name='wing-list'
    ),

    # Create Wing
    path(
        'create/',
        WingCreateAPIView.as_view(),
        name='wing-create'
    ),

    # Wing Detail
    path(
        '<int:pk>/',
        WingDetailAPIView.as_view(),
        name='wing-detail'
    ),

    # Update Wing
    path(
        '<int:pk>/update/',
        WingUpdateAPIView.as_view(),
        name='wing-update'
    ),

    # Deactivate Wing
    path(
        '<int:pk>/delete/',
        WingDeleteAPIView.as_view(),
        name='wing-delete'
    ),
]