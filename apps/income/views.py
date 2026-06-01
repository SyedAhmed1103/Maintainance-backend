from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Income
from .serializers import IncomeSerializer


# =========================================================
# CREATE INCOME
# =========================================================

class IncomeCreateAPIView(generics.CreateAPIView):

    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Income created successfully.",
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
# INCOME LIST
# =========================================================

class IncomeListAPIView(generics.ListAPIView):

    serializer_class = IncomeSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        queryset = Income.objects.select_related(
            'building'
        ).order_by('-income_date')

        if search:

            queryset = queryset.filter(
                Q(income_type__icontains=search) |
                Q(description__icontains=search) |
                Q(
                    building__building_name__icontains=search
                )
            )

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
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
                "message": "Income list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# INCOME DETAILS
# =========================================================

class IncomeDetailAPIView(generics.RetrieveAPIView):

    queryset = Income.objects.select_related(
        'building'
    )

    serializer_class = IncomeSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Income details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE INCOME
# =========================================================

class IncomeUpdateAPIView(generics.UpdateAPIView):

    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
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
                    "message": "Income updated successfully.",
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
# DELETE INCOME
# =========================================================

class IncomeDeleteAPIView(generics.DestroyAPIView):

    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Income deleted successfully."
            },
            status=status.HTTP_200_OK
        )