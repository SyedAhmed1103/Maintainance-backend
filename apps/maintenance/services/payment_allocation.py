from decimal import Decimal

from django.db import transaction
from django.db.models import Q, Case, When, Value, IntegerField
from django.core.exceptions import ValidationError

from apps.maintenance.models import (
    Payment,
    PaymentAdjustment,
    MaintenanceBill,
)


class PaymentAllocationService:

    @staticmethod
    def generate_receipt_number():

        last_payment = (
            Payment.objects
            .order_by('-id')
            .first()
        )

        next_id = 1

        if last_payment:
            next_id = last_payment.id + 1

        return f"RCPT-{next_id:06d}"

    @classmethod
    @transaction.atomic
    def receive_payment(
        cls,
        flat,
        amount,
        payment_mode,
        paid_at,
        transaction_id=None,
        remarks=None
    ):

        amount = Decimal(str(amount))

        if amount <= 0:

            raise ValidationError(
                "Payment amount must be greater than zero."
            )

        receipt_number = (
            cls.generate_receipt_number()
        )

        payment = Payment.objects.create(
            flat=flat,
            amount=amount,
            unallocated_amount=amount,
            receipt_number=receipt_number,
            payment_mode=payment_mode,
            transaction_id=transaction_id,
            remarks=remarks,
            paid_at=paid_at,
        )

        remaining_amount = amount

        pending_bills = (
            MaintenanceBill.objects
            .filter(
                flat=flat,
                is_active=True
            )
            .filter(
                Q(status='unpaid') |
                Q(status='partial')
            )
            .annotate(
                priority=Case(
                    When(
                        bill_type='opening',
                        then=Value(0)
                    ),
                    default=Value(1),
                    output_field=IntegerField()
                )
            )
            .order_by(
                'priority',
                'year',
                'month',
                'due_date',
                'id'
            )
        )

        for bill in pending_bills:

            if remaining_amount <= 0:
                break

            bill_pending = (
                bill.pending_amount
            )

            allocation_amount = min(
                remaining_amount,
                bill_pending
            )

            PaymentAdjustment.objects.create(
                payment=payment,
                bill=bill,
                adjusted_amount=allocation_amount
            )

            bill.paid_amount += allocation_amount

            bill.pending_amount -= allocation_amount

            if bill.pending_amount <= 0:

                bill.pending_amount = Decimal(
                    '0.00'
                )

                bill.status = 'paid'

            else:

                bill.status = 'partial'

            bill.save(
                update_fields=[
                    'paid_amount',
                    'pending_amount',
                    'status',
                    'updated_at'
                ]
            )

            remaining_amount -= allocation_amount

        payment.unallocated_amount = (
            remaining_amount
        )

        payment.save(
            update_fields=[
                'unallocated_amount',
                'updated_at'
            ]
        )

        return {
            "payment_id": payment.id,
            "receipt_number": payment.receipt_number,
            "payment_amount": payment.amount,
            "allocated_amount": (
                payment.amount -
                payment.unallocated_amount
            ),
            "advance_amount": (
                payment.unallocated_amount
            ),
            "status": "success"
        }

    @classmethod
    @transaction.atomic
    def auto_adjust_advance_balance(
        cls,
        bill
    ):

        available_payments = (
            Payment.objects
            .filter(
                flat=bill.flat,
                is_active=True,
                unallocated_amount__gt=0
            )
            .order_by(
                'paid_at',
                'id'
            )
        )

        remaining_due = (
            bill.pending_amount
        )

        for payment in available_payments:

            if remaining_due <= 0:
                break

            adjustment_amount = min(
                payment.unallocated_amount,
                remaining_due
            )

            PaymentAdjustment.objects.create(
                payment=payment,
                bill=bill,
                adjusted_amount=adjustment_amount
            )

            payment.unallocated_amount -= (
                adjustment_amount
            )

            payment.save(
                update_fields=[
                    'unallocated_amount',
                    'updated_at'
                ]
            )

            bill.paid_amount += (
                adjustment_amount
            )

            bill.pending_amount -= (
                adjustment_amount
            )

            remaining_due -= (
                adjustment_amount
            )

        if bill.pending_amount <= 0:

            bill.pending_amount = Decimal(
                '0.00'
            )

            bill.status = 'paid'

        elif bill.paid_amount > 0:

            bill.status = 'partial'

        else:

            bill.status = 'unpaid'

        bill.save(
            update_fields=[
                'paid_amount',
                'pending_amount',
                'status',
                'updated_at'
            ]
        )

        return bill