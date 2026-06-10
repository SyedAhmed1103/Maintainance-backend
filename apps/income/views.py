# views.py

from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Income
from .serializers import IncomeSerializer


class IncomeListAPIView(generics.ListAPIView):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        queryset = (
            Income.objects
            .filter(is_deleted=False)
            .select_related("building")
            .order_by("-income_date", "-id")
        )

        building_id = self.request.query_params.get("building_id")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        income_type = self.request.query_params.get("income_type")

        if building_id:
            queryset = queryset.filter(
                building_id=building_id
            )

        if year:
            queryset = queryset.filter(
                income_date__year=year
            )

        if month:
            queryset = queryset.filter(
                income_date__month=month
            )

        if income_type:
            queryset = queryset.filter(
                income_type__icontains=income_type
            )

        return queryset


class IncomeCreateAPIView(generics.CreateAPIView):
    serializer_class = IncomeSerializer

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
                "message": "Income created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class IncomeDetailAPIView(generics.RetrieveAPIView):
    serializer_class = IncomeSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return (
            Income.objects
            .filter(is_deleted=False)
            .select_related("building")
        )


class IncomeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = IncomeSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Income.objects.filter(
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
                "message": "Income updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class IncomeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = IncomeSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Income.objects.filter(
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
                "message": "Income deleted successfully."
            },
            status=status.HTTP_200_OK
        )