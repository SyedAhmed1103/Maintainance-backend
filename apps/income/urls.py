from django.urls import path

from .views import (
    IncomeListAPIView,
    IncomeCreateAPIView,
    IncomeDetailAPIView,
    IncomeUpdateAPIView,
    IncomeDeleteAPIView,
)

urlpatterns = [

    path(
        "list/",
        IncomeListAPIView.as_view(),
        name="income-list"
    ),

    path(
        "create/",
        IncomeCreateAPIView.as_view(),
        name="income-create"
    ),

    path(
        "<int:pk>/",
        IncomeDetailAPIView.as_view(),
        name="income-detail"
    ),

    path(
        "<int:pk>/update/",
        IncomeUpdateAPIView.as_view(),
        name="income-update"
    ),

    path(
        "<int:pk>/delete/",
        IncomeDeleteAPIView.as_view(),
        name="income-delete"
    ),
]