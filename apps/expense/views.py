from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Expense
from .serializers import ExpenseSerializer


# =========================================================
# CREATE EXPENSE
# =========================================================

class ExpenseCreateAPIView(generics.CreateAPIView):

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Expense created successfully.",
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
# EXPENSE LIST
# =========================================================

class ExpenseListAPIView(generics.ListAPIView):

    serializer_class = ExpenseSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        queryset = Expense.objects.select_related(
            'building'
        ).order_by('-expense_date')

        if search:

            queryset = queryset.filter(
                Q(expense_type__icontains=search) |
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
                "message": "Expense list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# EXPENSE DETAILS
# =========================================================

class ExpenseDetailAPIView(generics.RetrieveAPIView):

    queryset = Expense.objects.select_related(
        'building'
    )

    serializer_class = ExpenseSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Expense details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE EXPENSE
# =========================================================

class ExpenseUpdateAPIView(generics.UpdateAPIView):

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
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
                    "message": "Expense updated successfully.",
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
# DELETE EXPENSE
# =========================================================

class ExpenseDeleteAPIView(generics.DestroyAPIView):

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Expense deleted successfully."
            },
            status=status.HTTP_200_OK
        )