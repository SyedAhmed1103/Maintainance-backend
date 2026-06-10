from django.urls import path

from .views import (
    ExpenseListAPIView,
    ExpenseCreateAPIView,
    ExpenseDetailAPIView,
    ExpenseUpdateAPIView,
    ExpenseDeleteAPIView,
)

urlpatterns = [

    path(
        "list/",
        ExpenseListAPIView.as_view(),
        name="expense-list"
    ),

    path(
        "create/",
        ExpenseCreateAPIView.as_view(),
        name="expense-create"
    ),

    path(
        "<int:pk>/",
        ExpenseDetailAPIView.as_view(),
        name="expense-detail"
    ),

    path(
        "<int:pk>/update/",
        ExpenseUpdateAPIView.as_view(),
        name="expense-update"
    ),

    path(
        "<int:pk>/delete/",
        ExpenseDeleteAPIView.as_view(),
        name="expense-delete"
    ),
]