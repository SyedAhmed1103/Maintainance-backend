from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.maintenance.services.receipt_service import (
    ReceiptService
)


# =========================================================
# RECEIPT DETAIL
# =========================================================

class ReceiptDetailAPIView(
    APIView
):

    def get(
        self,
        request,
        payment_id
    ):

        try:

            data = (
                ReceiptService
                .get_receipt_data(
                    payment_id
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Receipt fetched successfully.",
                    "data": data
                },
                status=status.HTTP_200_OK
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
# RECEIPT SUMMARY
# =========================================================

class ReceiptSummaryAPIView(
    APIView
):

    def get(
        self,
        request,
        payment_id
    ):

        try:

            data = (
                ReceiptService
                .get_receipt_summary(
                    payment_id
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Receipt summary fetched successfully.",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )