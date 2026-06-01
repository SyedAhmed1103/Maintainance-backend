from django.urls import path

from .views import (
    NoticeCreateAPIView,
    NoticeListAPIView,
    NoticeDetailAPIView,
    NoticeUpdateAPIView,
    NoticeDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE NOTICE
    # ==================================================

    path(
        'create/',
        NoticeCreateAPIView.as_view(),
        name='notice-create'
    ),

    # ==================================================
    # NOTICE LIST
    # ==================================================

    path(
        '',
        NoticeListAPIView.as_view(),
        name='notice-list'
    ),

    # ==================================================
    # NOTICE DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        NoticeDetailAPIView.as_view(),
        name='notice-detail'
    ),

    # ==================================================
    # UPDATE NOTICE
    # ==================================================

    path(
        'update/<int:pk>/',
        NoticeUpdateAPIView.as_view(),
        name='notice-update'
    ),

    # ==================================================
    # DELETE NOTICE
    # ==================================================

    path(
        'delete/<int:pk>/',
        NoticeDeleteAPIView.as_view(),
        name='notice-delete'
    ),
]