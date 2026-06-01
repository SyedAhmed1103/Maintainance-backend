from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer


# =========================================================
# CREATE PAYMENT
# =========================================================

class PaymentCreateAPIView(
    generics.CreateAPIView
):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": (
                        "Payment created successfully."
                    ),
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "message": "Validation error.",
                "errors": serializer.errors
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

        search = self.request.GET.get(
            'search',
            ''
        )

        status_filter = self.request.GET.get(
            'status',
            ''
        )

        payment_mode = self.request.GET.get(
            'payment_mode',
            ''
        )

        user_id = self.request.GET.get(
            'user_id',
            ''
        )

        flat_id = self.request.GET.get(
            'flat_id',
            ''
        )

        queryset = (
            Payment.objects
            .select_related(
                'maintenance_detail',
                'user',
                'flat'
            )
            .order_by('-payment_date')
        )

        if search:

            queryset = queryset.filter(
                Q(receipt_number__icontains=search) |
                Q(transaction_id__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
            )

        if payment_mode:

            queryset = queryset.filter(
                payment_mode=payment_mode
            )

        if user_id:

            queryset = queryset.filter(
                user_id=user_id
            )

        if flat_id:

            queryset = queryset.filter(
                flat_id=flat_id
            )

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Payments fetched successfully."
                ),
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PAYMENT DETAILS
# =========================================================

class PaymentDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        Payment.objects
        .select_related(
            'maintenance_detail',
            'user',
            'flat'
        )
    )

    serializer_class = PaymentSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Payment details fetched successfully."
                ),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE PAYMENT
# =========================================================

class PaymentUpdateAPIView(
    generics.UpdateAPIView
):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop(
            'partial',
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": (
                        "Payment updated successfully."
                    ),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "message": "Validation error.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):

        kwargs['partial'] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# DELETE PAYMENT
# =========================================================

class PaymentDeleteAPIView(
    generics.DestroyAPIView
):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Payment deleted successfully."
                )
            },
            status=status.HTTP_200_OK
        )