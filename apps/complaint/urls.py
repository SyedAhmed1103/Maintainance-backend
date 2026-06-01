from django.urls import path

from .views import (
    ComplaintCreateAPIView,
    ComplaintListAPIView,
    ComplaintDetailAPIView,
    ComplaintUpdateAPIView,
    ComplaintDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE COMPLAINT
    # ==================================================

    path(
        'create/',
        ComplaintCreateAPIView.as_view(),
        name='complaint-create'
    ),

    # ==================================================
    # COMPLAINT LIST
    # ==================================================

    path(
        '',
        ComplaintListAPIView.as_view(),
        name='complaint-list'
    ),

    # ==================================================
    # COMPLAINT DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        ComplaintDetailAPIView.as_view(),
        name='complaint-detail'
    ),

    # ==================================================
    # UPDATE COMPLAINT
    # ==================================================

    path(
        'update/<int:pk>/',
        ComplaintUpdateAPIView.as_view(),
        name='complaint-update'
    ),

    # ==================================================
    # DELETE COMPLAINT
    # ==================================================

    path(
        'delete/<int:pk>/',
        ComplaintDeleteAPIView.as_view(),
        name='complaint-delete'
    ),
]