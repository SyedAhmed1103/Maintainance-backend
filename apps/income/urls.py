from django.urls import path

from .views import (
    IncomeCreateAPIView,
    IncomeListAPIView,
    IncomeDetailAPIView,
    IncomeUpdateAPIView,
    IncomeDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE INCOME
    # ==================================================

    path(
        'create/',
        IncomeCreateAPIView.as_view(),
        name='income-create'
    ),

    # ==================================================
    # INCOME LIST
    # ==================================================

    path(
        '',
        IncomeListAPIView.as_view(),
        name='income-list'
    ),

    # ==================================================
    # INCOME DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        IncomeDetailAPIView.as_view(),
        name='income-detail'
    ),

    # ==================================================
    # UPDATE INCOME
    # ==================================================

    path(
        'update/<int:pk>/',
        IncomeUpdateAPIView.as_view(),
        name='income-update'
    ),

    # ==================================================
    # DELETE INCOME
    # ==================================================

    path(
        'delete/<int:pk>/',
        IncomeDeleteAPIView.as_view(),
        name='income-delete'
    ),
]