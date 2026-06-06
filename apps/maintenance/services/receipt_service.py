from django.core.exceptions import ValidationError

from apps.maintenance.models import Payment


class ReceiptService:

    @staticmethod
    def get_receipt_data(
        payment_id
    ):

        try:

            payment = (
                Payment.objects
                .select_related(
                    'flat',
                    'flat__building'
                )
                .prefetch_related(
                    'adjustments',
                    'adjustments__bill'
                )
                .get(
                    id=payment_id,
                    is_active=True
                )
            )

        except Payment.DoesNotExist:

            raise ValidationError(
                "Payment not found."
            )

        flat = payment.flat
        building = flat.building

        adjustments = []

        total_allocated = 0

        for adjustment in (
            payment.adjustments.all()
        ):

            total_allocated += (
                adjustment.adjusted_amount
            )

            adjustments.append({
                "bill_id":
                adjustment.bill.id,

                "bill_type":
                adjustment.bill.bill_type,

                "month":
                adjustment.bill.month,

                "year":
                adjustment.bill.year,

                "adjusted_amount":
                adjustment.adjusted_amount,
            })

        return {

            "receipt_number":
            payment.receipt_number,

            "payment_id":
            payment.id,

            "building_name":
            building.building_name,

            "flat_number":
            flat.flat_number,

            "wing":
            flat.wing.wing_name if flat.wing else None,

            "payment_amount":
            payment.amount,

            "allocated_amount":
            total_allocated,

            "advance_amount":
            payment.unallocated_amount,

            "payment_mode":
            payment.payment_mode,

            "transaction_id":
            payment.transaction_id,

            "remarks":
            payment.remarks,

            "paid_at":
            payment.paid_at,

            "adjustments":
            adjustments,
        }

    @classmethod
    def get_receipt_summary(
        cls,
        payment_id
    ):

        data = cls.get_receipt_data(
            payment_id
        )

        return {

            "receipt_number":
            data["receipt_number"],

            "flat_number":
            data["flat_number"],

            "payment_amount":
            data["payment_amount"],

            "allocated_amount":
            data["allocated_amount"],

            "advance_amount":
            data["advance_amount"],

            "paid_at":
            data["paid_at"],
        }