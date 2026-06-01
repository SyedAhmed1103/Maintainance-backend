from django.urls import path

from .views import (
    ExpenseCreateAPIView,
    ExpenseListAPIView,
    ExpenseDetailAPIView,
    ExpenseUpdateAPIView,
    ExpenseDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE EXPENSE
    # ==================================================

    path(
        'create/',
        ExpenseCreateAPIView.as_view(),
        name='expense-create'
    ),

    # ==================================================
    # EXPENSE LIST
    # ==================================================

    path(
        '',
        ExpenseListAPIView.as_view(),
        name='expense-list'
    ),

    # ==================================================
    # EXPENSE DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        ExpenseDetailAPIView.as_view(),
        name='expense-detail'
    ),

    # ==================================================
    # UPDATE EXPENSE
    # ==================================================

    path(
        'update/<int:pk>/',
        ExpenseUpdateAPIView.as_view(),
        name='expense-update'
    ),

    # ==================================================
    # DELETE EXPENSE
    # ==================================================

    path(
        'delete/<int:pk>/',
        ExpenseDeleteAPIView.as_view(),
        name='expense-delete'
    ),
]