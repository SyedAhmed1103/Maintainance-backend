from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.flats.models import Flat

from apps.maintenance.models import (
    Payment
)

from apps.maintenance.services.payment_allocation import (
    PaymentAllocationService
)

from apps.maintenance.serializers.payment_serializers import (
    PaymentSerializer,
    PaymentReceiveRequestSerializer
)


# =========================================================
# RECEIVE PAYMENT
# =========================================================

class ReceivePaymentAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = (
            PaymentReceiveRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        try:

            flat = Flat.objects.get(
                id=data['flat_id'],
                is_active=True
            )

        except Flat.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Flat not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            result = (
                PaymentAllocationService
                .receive_payment(
                    flat=flat,
                    amount=data['amount'],
                    payment_mode=data['payment_mode'],
                    paid_at=data['paid_at'],
                    transaction_id=data.get(
                        'transaction_id'
                    ),
                    remarks=data.get(
                        'remarks'
                    )
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Payment received successfully.",
                    "data": result
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# =========================================================
# PAYMENT LIST
# =========================================================

class PaymentListAPIView(
    generics.ListAPIView
):

    serializer_class = PaymentSerializer

    def get_queryset(self):

        flat_id = self.request.GET.get(
            'flat_id'
        )

        queryset = (
            Payment.objects
            .select_related(
                'flat',
                'flat__building'
            )
            .order_by(
                '-paid_at'
            )
        )

        if flat_id:

            queryset = queryset.filter(
                flat_id=flat_id
            )

        return queryset

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PAYMENT DETAIL
# =========================================================

class PaymentDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        Payment.objects
        .select_related(
            'flat',
            'flat__building'
        )
    )

    serializer_class = PaymentSerializer

    lookup_field = 'pk'

    def retrieve(
        self,
        request,
        *args,
        **kwargs
    ):

        payment = self.get_object()

        serializer = self.get_serializer(
            payment
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# FLAT PAYMENT HISTORY
# =========================================================

class FlatPaymentHistoryAPIView(
    generics.ListAPIView
):

    serializer_class = PaymentSerializer

    def get_queryset(self):

        flat_id = self.kwargs.get(
            'flat_id'
        )

        return (
            Payment.objects
            .filter(
                flat_id=flat_id
            )
            .select_related(
                'flat',
                'flat__building'
            )
            .order_by(
                '-paid_at'
            )
        )

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )