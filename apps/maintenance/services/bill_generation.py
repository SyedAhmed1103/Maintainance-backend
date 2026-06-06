from decimal import Decimal
from datetime import date

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.maintenance.models import (
    MaintenanceConfig,
    MaintenanceBill,
)
from apps.maintenance.services.payment_allocation import (
    PaymentAllocationService
)

from apps.flats.models import Flat


class BillGenerationService:

    @staticmethod
    def get_applicable_config(
        building,
        bill_date
    ):
        config = (
            MaintenanceConfig.objects
            .filter(
                building=building,
                is_active=True,
                effective_from__lte=bill_date
            )
            .order_by('-effective_from')
            .first()
        )

        if not config:

            raise ValidationError(
                "No applicable maintenance configuration found."
            )

        return config

    @staticmethod
    def calculate_bill_amount(
        flat,
        config
    ):

        if config.calculation_type == 'fixed':

            return config.fixed_amount

        if config.calculation_type == 'per_sqft':

            if not flat.area_sqft:

                raise ValidationError(
                    f"Area not configured for Flat "
                    f"{flat.flat_number}"
                )

            return (
                Decimal(flat.area_sqft)
                * Decimal(config.rate_per_sqft)
            )

        raise ValidationError(
            "Invalid calculation type."
        )

    @classmethod
    @transaction.atomic
    def generate_monthly_bills(
        cls,
        building,
        month,
        year,
        due_date,
        notes=None
    ):

        if month < 1 or month > 12:

            raise ValidationError(
                "Invalid month."
            )

        if year < 2000:

            raise ValidationError(
                "Invalid year."
            )

        bill_date = date(
            year,
            month,
            1
        )

        config = cls.get_applicable_config(
            building,
            bill_date
        )

        flats = Flat.objects.filter(
            building=building,
            is_active=True
        ).exclude(
            occupancy_status='unsold'
        )

        existing_flat_ids = set(
            MaintenanceBill.objects.filter(
                bill_type='monthly',
                month=month,
                year=year,
                is_active=True,
                flat__building=building
            ).values_list(
                'flat_id',
                flat=True
            )
        )

        bills_to_create = []

        skipped_flat_ids = []

        for flat in flats:

            if flat.id in existing_flat_ids:

                skipped_flat_ids.append(
                    flat.id
                )
                continue

            amount = cls.calculate_bill_amount(
                flat,
                config
            )

            bills_to_create.append(
                MaintenanceBill(
                    flat=flat,
                    bill_type='monthly',
                    month=month,
                    year=year,
                    amount=amount,
                    paid_amount=Decimal('0.00'),
                    pending_amount=amount,
                    due_date=due_date,
                    status='unpaid',
                    notes=notes or ''
                )
            )

        created_bills = (
            MaintenanceBill.objects.bulk_create(
                bills_to_create
            )
        )

        for bill in created_bills:
            PaymentAllocationService.auto_adjust_advance_balance(
                bill
            )

        return {
            "created_count": len(
                created_bills
            ),
            "skipped_count": len(
                skipped_flat_ids
            ),
            "skipped_flat_ids":
            skipped_flat_ids
        }

    @classmethod
    @transaction.atomic
    def create_opening_due(
        cls,
        flat,
        amount,
        due_date,
        notes=None
    ):

        exists = (
            MaintenanceBill.objects
            .filter(
                flat=flat,
                bill_type='opening',
                is_active=True
            )
            .exists()
        )

        if exists:

            raise ValidationError(
                "Opening due already exists."
            )

        return (
            MaintenanceBill.objects.create(
                flat=flat,
                bill_type='opening',
                amount=amount,
                paid_amount=Decimal('0.00'),
                pending_amount=amount,
                due_date=due_date,
                status='unpaid',
                notes=notes or ''
            )
        )

    @classmethod
    @transaction.atomic
    def create_special_charge(
        cls,
        flat,
        amount,
        due_date,
        notes=None
    ):

        bill = MaintenanceBill.objects.create(
            flat=flat,
            bill_type='special',
            amount=amount,
            paid_amount=Decimal('0.00'),
            pending_amount=amount,
            due_date=due_date,
            status='unpaid',
            notes=notes or ''
        )

        PaymentAllocationService.auto_adjust_advance_balance(
            bill
        )

        return bill

    @classmethod
    @transaction.atomic
    def bulk_special_charge(
        cls,
        building,
        amount,
        due_date,
        notes=None
    ):

        flats = Flat.objects.filter(
            building=building,
            is_active=True
        ).exclude(
            occupancy_status='unsold'
        )

        bills = []

        for flat in flats:

            bills.append(
                MaintenanceBill(
                    flat=flat,
                    bill_type='special',
                    amount=amount,
                    paid_amount=Decimal('0.00'),
                    pending_amount=amount,
                    due_date=due_date,
                    status='unpaid',
                    notes=notes or ''
                )
            )

        created = (
            MaintenanceBill.objects.bulk_create(
                bills
            )
        )

        for bill in created:
            PaymentAllocationService.auto_adjust_advance_balance(
                bill
            )

        return {
            "created_count": len(created)
        }