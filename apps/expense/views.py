# views.py

from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseListAPIView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = (
            Expense.objects
            .filter(is_deleted=False)
            .select_related("building")
            .order_by("-expense_date", "-id")
        )

        building_id = self.request.query_params.get("building_id")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        expense_type = self.request.query_params.get("expense_type")

        if building_id:
            queryset = queryset.filter(
                building_id=building_id
            )

        if year:
            queryset = queryset.filter(
                expense_date__year=year
            )

        if month:
            queryset = queryset.filter(
                expense_date__month=month
            )

        if expense_type:
            queryset = queryset.filter(
                expense_type__icontains=expense_type
            )

        return queryset


class ExpenseCreateAPIView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Expense created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class ExpenseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ExpenseSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return (
            Expense.objects
            .filter(is_deleted=False)
            .select_related("building")
        )


class ExpenseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Expense.objects.filter(
            is_deleted=False
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Expense updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class ExpenseDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ExpenseSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Expense.objects.filter(
            is_deleted=False
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.is_deleted = True
        instance.deleted_at = timezone.now()

        instance.save(
            update_fields=[
                "is_deleted",
                "deleted_at"
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Expense deleted successfully."
            },
            status=status.HTTP_200_OK
        )