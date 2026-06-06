from django.db.models import Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.building.models import Building
from apps.maintenance.models import (
    MaintenanceBill
)

from apps.maintenance.services.bill_generation import (
    BillGenerationService
)

from apps.maintenance.serializers.bill_serializers import (
    MaintenanceBillSerializer
)


# =========================================================
# GENERATE MONTHLY BILLS
# =========================================================

class GenerateMonthlyBillsAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        building_id = request.data.get(
            'building_id'
        )

        month = request.data.get(
            'month'
        )

        year = request.data.get(
            'year'
        )

        due_date = request.data.get(
            'due_date'
        )

        notes = request.data.get(
            'notes'
        )

        if not building_id:

            return Response(
                {
                    "success": False,
                    "message":
                    "Building id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            building = Building.objects.get(
                id=building_id,
                is_active=True
            )

        except Building.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                    "Building not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            result = (
                BillGenerationService
                .generate_monthly_bills(
                    building=building,
                    month=int(month),
                    year=int(year),
                    due_date=due_date,
                    notes=notes
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Bills generated successfully.",
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
# BILL LIST
# =========================================================

class MaintenanceBillListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MaintenanceBillSerializer
    )

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        flat_id = self.request.GET.get(
            'flat_id',
            ''
        )

        status_filter = self.request.GET.get(
            'status',
            ''
        )

        queryset = (
            MaintenanceBill.objects
            .select_related(
                'flat',
                'flat__building'
            )
            .order_by(
                '-year',
                '-month',
                '-id'
            )
        )

        if search:

            queryset = queryset.filter(
                Q(
                    flat__flat_number__icontains=search
                )
            )

        if building_id:

            queryset = queryset.filter(
                flat__building_id=building_id
            )

        if flat_id:

            queryset = queryset.filter(
                flat_id=flat_id
            )

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
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
# BILL DETAIL
# =========================================================

class MaintenanceBillDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        MaintenanceBill.objects
        .select_related(
            'flat',
            'flat__building'
        )
    )

    serializer_class = (
        MaintenanceBillSerializer
    )

    lookup_field = 'pk'

    def retrieve(
        self,
        request,
        *args,
        **kwargs
    ):

        bill = self.get_object()

        serializer = self.get_serializer(
            bill
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# FLAT BILL LIST
# =========================================================

class FlatBillListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MaintenanceBillSerializer
    )

    def get_queryset(self):

        flat_id = self.kwargs.get(
            'flat_id'
        )

        return (
            MaintenanceBill.objects
            .filter(
                flat_id=flat_id
            )
            .select_related(
                'flat',
                'flat__building'
            )
            .order_by(
                '-year',
                '-month'
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
    

# =========================================================
# GENERATE SPECIAL BILL
# =========================================================

class GenerateSpecialBillAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        building_id = request.data.get(
            'building_id'
        )

        amount = request.data.get(
            'amount'
        )

        due_date = request.data.get(
            'due_date'
        )

        notes = request.data.get(
            'notes'
        )

        if not building_id:

            return Response(
                {
                    "success": False,
                    "message":
                    "Building id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            building = Building.objects.get(
                id=building_id,
                is_active=True
            )

        except Building.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                    "Building not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            result = (
                BillGenerationService
                .bulk_special_charge(
                    building=building,
                    amount=amount,
                    due_date=due_date,
                    notes=notes
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Special bills generated successfully.",
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
# GENERATE SPECIAL BILL FOR FLAT
# =========================================================

from apps.flats.models import Flat

class GenerateFlatSpecialBillAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        flat_id = request.data.get(
            'flat_id'
        )

        amount = request.data.get(
            'amount'
        )

        due_date = request.data.get(
            'due_date'
        )

        notes = request.data.get(
            'notes'
        )

        if not flat_id:

            return Response(
                {
                    "success": False,
                    "message":
                    "Flat id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            flat = Flat.objects.get(
                id=flat_id,
                is_active=True
            )

        except Flat.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                    "Flat not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            bill = (
                BillGenerationService
                .create_special_charge(
                    flat=flat,
                    amount=amount,
                    due_date=due_date,
                    notes=notes
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Special bill created successfully.",
                    "data": {
                        "bill_id": bill.id
                    }
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
        

from apps.flats.models import Flat
from apps.maintenance.models import Payment

class GenerateOpeningBillAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        flat_id = request.data.get(
            'flat_id'
        )

        amount = request.data.get(
            'amount'
        )

        due_date = request.data.get(
            'due_date'
        )

        notes = request.data.get(
            'notes'
        )

        try:

            flat = Flat.objects.get(
                id=flat_id,
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

        if Payment.objects.filter(
            flat=flat,
            is_active=True
        ).exists():

            return Response(
                {
                    "success": False,
                    "message":
                    "Opening due cannot be created after payments exist."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            bill = (
                BillGenerationService
                .create_opening_due(
                    flat=flat,
                    amount=amount,
                    due_date=due_date,
                    notes=notes
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                    "Opening bill created successfully.",
                    "data": {
                        "bill_id": bill.id
                    }
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
        


from apps.maintenance.models import (
    MaintenanceBill,
    Payment
)

class UpdateOpeningBillAPIView(
    APIView
):

    def put(
        self,
        request,
        bill_id
    ):

        try:

            bill = (
                MaintenanceBill.objects.get(
                    id=bill_id,
                    bill_type='opening',
                    is_active=True
                )
            )

        except MaintenanceBill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                    "Opening bill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Flat par ek bhi payment aa gayi ho
        if Payment.objects.filter(
            flat=bill.flat,
            is_active=True
        ).exists():

            return Response(
                {
                    "success": False,
                    "message":
                    "Opening bill cannot be updated after payments exist."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = request.data.get(
            'amount',
            bill.amount
        )

        due_date = request.data.get(
            'due_date',
            bill.due_date
        )

        notes = request.data.get(
            'notes',
            bill.notes
        )

        bill.amount = amount
        bill.pending_amount = amount
        bill.due_date = due_date
        bill.notes = notes

        bill.save(
            update_fields=[
                'amount',
                'pending_amount',
                'due_date',
                'notes',
                'updated_at'
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "Opening bill updated successfully.",
                "data": {
                    "bill_id": bill.id
                }
            },
            status=status.HTTP_200_OK
        )