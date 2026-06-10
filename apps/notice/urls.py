from django.urls import path

from .views import (
    NoticeCreateAPIView,
    NoticeListAPIView,
    BuildingNoticeListAPIView,
    NoticeDetailAPIView,
    NoticeUpdateAPIView,
    NoticeDeleteAPIView,
)

urlpatterns = [

    path(
        "create/",
        NoticeCreateAPIView.as_view(),
        name="notice-create"
    ),

    path(
        "",
        NoticeListAPIView.as_view(),
        name="notice-list"
    ),

    path(
        "building/<int:building_id>/",
        BuildingNoticeListAPIView.as_view(),
        name="building-notice-list"
    ),

    path(
        "<int:pk>/",
        NoticeDetailAPIView.as_view(),
        name="notice-detail"
    ),

    path(
        "<int:pk>/update/",
        NoticeUpdateAPIView.as_view(),
        name="notice-update"
    ),

    path(
        "<int:pk>/delete/",
        NoticeDeleteAPIView.as_view(),
        name="notice-delete"
    ),

]