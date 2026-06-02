from django.urls import path

from .views import (
    WingCreateAPIView,
    WingListAPIView,
    WingDetailAPIView,
    WingUpdateAPIView,
    WingDeleteAPIView
)

urlpatterns = [
    
    path(
        'create/',
        WingCreateAPIView.as_view(),
        name='wing-create'
    ),

    path(
        'list/',
        WingListAPIView.as_view(),
        name='wing-list'
    ),

    path(
        'detail/<int:pk>/',
        WingDetailAPIView.as_view(),
        name='wing-detail'
    ),

    path(
        'update/<int:pk>/',
        WingUpdateAPIView.as_view(),
        name='wing-update'
    ),

    path(
        'delete/<int:pk>/',
        WingDeleteAPIView.as_view(),
        name='wing-delete'
    ),

]