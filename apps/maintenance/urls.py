from django.urls import path

from .views.config_views import (
    MaintenanceConfigCreateAPIView,
    MaintenanceConfigListAPIView,
    MaintenanceConfigDetailAPIView,
    MaintenanceConfigUpdateAPIView,
    MaintenanceConfigDeleteAPIView,
)

from .views.bill_views import (
    GenerateMonthlyBillsAPIView,
    GenerateSpecialBillAPIView,
    GenerateFlatSpecialBillAPIView,
    GenerateOpeningBillAPIView,
    UpdateOpeningBillAPIView,
    MaintenanceBillListAPIView,
    MaintenanceBillDetailAPIView,
    FlatBillListAPIView,
)

from .views.payment_views import (
    ReceivePaymentAPIView,
    PaymentListAPIView,
    PaymentDetailAPIView,
    FlatPaymentHistoryAPIView,
)

from .views.receipt_views import (
    ReceiptDetailAPIView,
    ReceiptSummaryAPIView,
)

urlpatterns = [

    # ==================================================
    # MAINTENANCE CONFIG
    # ==================================================

    path(
        'configs/create/',
        MaintenanceConfigCreateAPIView.as_view(),
        name='maintenance-config-create'
    ),

    path(
        'configs/',
        MaintenanceConfigListAPIView.as_view(),
        name='maintenance-config-list'
    ),

    path(
        'configs/<int:pk>/',
        MaintenanceConfigDetailAPIView.as_view(),
        name='maintenance-config-detail'
    ),

    path(
        'configs/update/<int:pk>/',
        MaintenanceConfigUpdateAPIView.as_view(),
        name='maintenance-config-update'
    ),

    path(
        'configs/delete/<int:pk>/',
        MaintenanceConfigDeleteAPIView.as_view(),
        name='maintenance-config-delete'
    ),

    # ==================================================
    # MAINTENANCE BILLS
    # ==================================================

    path(
        'bills/generate/',
        GenerateMonthlyBillsAPIView.as_view(),
        name='bill-generate'
    ),

    path(
        'bills/special/generate/',
        GenerateSpecialBillAPIView.as_view(),
        name='special-bill-generate'
    ),
    path(
        'bills/flatspecial/generate/',
        GenerateFlatSpecialBillAPIView.as_view(),
        name='special-bill-create'
    ),
    path(
        'bills/opening/generate/',
        GenerateOpeningBillAPIView.as_view(),
        name='opening-bill-create'
    ),
    path(
        'bills/opening/update/<int:bill_id>/',
        UpdateOpeningBillAPIView.as_view(),
        name='opening-bill-update'
    ),

    path(
        'bills/',
        MaintenanceBillListAPIView.as_view(),
        name='bill-list'
    ),

    path(
        'bills/<int:pk>/',
        MaintenanceBillDetailAPIView.as_view(),
        name='bill-detail'
    ),

    path(
        'bills/flat/<int:flat_id>/',
        FlatBillListAPIView.as_view(),
        name='flat-bill-list'
    ),

    # ==================================================
    # PAYMENTS
    # ==================================================

    path(
        'payments/receive/',
        ReceivePaymentAPIView.as_view(),
        name='payment-receive'
    ),

    path(
        'payments/',
        PaymentListAPIView.as_view(),
        name='payment-list'
    ),

    path(
        'payments/<int:pk>/',
        PaymentDetailAPIView.as_view(),
        name='payment-detail'
    ),

    path(
        'payments/flat/<int:flat_id>/',
        FlatPaymentHistoryAPIView.as_view(),
        name='flat-payment-history'
    ),

    # ==================================================
    # RECEIPTS
    # ==================================================

    path(
        'receipts/<int:payment_id>/',
        ReceiptDetailAPIView.as_view(),
        name='receipt-detail'
    ),

    path(
        'receipts/<int:payment_id>/summary/',
        ReceiptSummaryAPIView.as_view(),
        name='receipt-summary'
    ),

]