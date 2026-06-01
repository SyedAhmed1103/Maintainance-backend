from django.urls import path

from .views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentDetailAPIView,
    PaymentUpdateAPIView,
    PaymentDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # CREATE PAYMENT
    # ==================================================

    path(
        'create/',
        PaymentCreateAPIView.as_view(),
        name='payment-create'
    ),

    # ==================================================
    # PAYMENT LIST
    # ==================================================

    path(
        '',
        PaymentListAPIView.as_view(),
        name='payment-list'
    ),

    # ==================================================
    # PAYMENT DETAILS
    # ==================================================

    path(
        '<int:pk>/',
        PaymentDetailAPIView.as_view(),
        name='payment-detail'
    ),

    # ==================================================
    # UPDATE PAYMENT
    # ==================================================

    path(
        'update/<int:pk>/',
        PaymentUpdateAPIView.as_view(),
        name='payment-update'
    ),

    # ==================================================
    # DELETE PAYMENT
    # ==================================================

    path(
        'delete/<int:pk>/',
        PaymentDeleteAPIView.as_view(),
        name='payment-delete'
    ),
]