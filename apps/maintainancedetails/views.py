from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import MaintenanceDetail
from .serializers import MaintenanceDetailSerializer


# =========================================================
# CREATE MAINTENANCE DETAIL
# =========================================================

class MaintenanceDetailCreateAPIView(
    generics.CreateAPIView
):

    queryset = MaintenanceDetail.objects.all()
    serializer_class = MaintenanceDetailSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": (
                        "Maintenance detail created successfully."
                    ),
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
# MAINTENANCE DETAIL LIST
# =========================================================

class MaintenanceDetailListAPIView(
    generics.ListAPIView
):

    serializer_class = MaintenanceDetailSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        maintenance_id = self.request.GET.get(
            'maintenance_id',
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
            MaintenanceDetail.objects
            .select_related(
                'maintenance',
                'flat',
                'flat__building'
            )
            .order_by('-id')
        )

        if search:

            queryset = queryset.filter(
                Q(flat__flat_number__icontains=search) |
                Q(flat__wing__icontains=search) |
                Q(
                    maintenance__title__icontains=search
                ) |
                Q(
                    flat__building__building_name__icontains=search
                )
            )

        if maintenance_id:

            queryset = queryset.filter(
                maintenance_id=maintenance_id
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

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance details fetched successfully."
                ),
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# MAINTENANCE DETAIL DETAILS
# =========================================================

class MaintenanceDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        MaintenanceDetail.objects
        .select_related(
            'maintenance',
            'flat',
            'flat__building'
        )
    )

    serializer_class = MaintenanceDetailSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance detail fetched successfully."
                ),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE MAINTENANCE DETAIL
# =========================================================

class MaintenanceDetailUpdateAPIView(
    generics.UpdateAPIView
):

    queryset = MaintenanceDetail.objects.all()
    serializer_class = MaintenanceDetailSerializer
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
                    "message": (
                        "Maintenance detail updated successfully."
                    ),
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
# DELETE MAINTENANCE DETAIL
# =========================================================

class MaintenanceDetailDeleteAPIView(
    generics.DestroyAPIView
):

    queryset = MaintenanceDetail.objects.all()
    serializer_class = MaintenanceDetailSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance detail deleted successfully."
                )
            },
            status=status.HTTP_200_OK
        )