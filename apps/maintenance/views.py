from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Maintenance
from .serializers import MaintenanceSerializer


# =========================================================
# CREATE MAINTENANCE
# =========================================================

class MaintenanceCreateAPIView(generics.CreateAPIView):

    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Maintenance created successfully.",
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
# MAINTENANCE LIST
# =========================================================

class MaintenanceListAPIView(generics.ListAPIView):

    serializer_class = MaintenanceSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        month = self.request.GET.get(
            'month',
            ''
        )

        year = self.request.GET.get(
            'year',
            ''
        )

        status_filter = self.request.GET.get(
            'status',
            ''
        )

        queryset = Maintenance.objects.select_related(
            'building'
        ).order_by(
            '-year',
            '-month'
        )

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(building__building_name__icontains=search)
            )

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
            )

        if month:

            queryset = queryset.filter(
                month=month
            )

        if year:

            queryset = queryset.filter(
                year=year
            )

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
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
                "message": "Maintenance list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# MAINTENANCE DETAILS
# =========================================================

class MaintenanceDetailAPIView(generics.RetrieveAPIView):

    queryset = Maintenance.objects.select_related(
        'building'
    )

    serializer_class = MaintenanceSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Maintenance details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE MAINTENANCE
# =========================================================

class MaintenanceUpdateAPIView(generics.UpdateAPIView):

    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
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
                    "message": "Maintenance updated successfully.",
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
# DELETE MAINTENANCE
# =========================================================

class MaintenanceDeleteAPIView(generics.DestroyAPIView):

    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Maintenance deleted successfully."
            },
            status=status.HTTP_200_OK
        )