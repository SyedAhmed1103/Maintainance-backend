from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..models import MaintenanceConfig
from ..serializers.config_serializers import MaintenanceConfigSerializer


# =========================================================
# CREATE CONFIG
# =========================================================

class MaintenanceConfigCreateAPIView(
    generics.CreateAPIView
):

    queryset = MaintenanceConfig.objects.all()
    serializer_class = (
        MaintenanceConfigSerializer
    )

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": (
                        "Maintenance configuration "
                        "created successfully."
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
# CONFIG LIST
# =========================================================

class MaintenanceConfigListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MaintenanceConfigSerializer
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

        is_active = self.request.GET.get(
            'is_active',
            ''
        )

        queryset = (
            MaintenanceConfig.objects
            .select_related('building')
            .order_by('-effective_from')
        )

        if search:

            queryset = queryset.filter(
                Q(
                    building__building_name__icontains=search
                )
            )

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
            )

        if is_active != '':

            if is_active.lower() == 'true':

                queryset = queryset.filter(
                    is_active=True
                )

            elif is_active.lower() == 'false':

                queryset = queryset.filter(
                    is_active=False
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
                "message": (
                    "Maintenance configurations "
                    "fetched successfully."
                ),
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# CONFIG DETAIL
# =========================================================

class MaintenanceConfigDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        MaintenanceConfig.objects
        .select_related('building')
    )

    serializer_class = (
        MaintenanceConfigSerializer
    )

    lookup_field = 'pk'

    def retrieve(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance configuration "
                    "fetched successfully."
                ),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE CONFIG
# =========================================================

class MaintenanceConfigUpdateAPIView(
    generics.UpdateAPIView
):

    queryset = (
        MaintenanceConfig.objects.all()
    )

    serializer_class = (
        MaintenanceConfigSerializer
    )

    lookup_field = 'pk'

    def update(
        self,
        request,
        *args,
        **kwargs
    ):

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
                        "Maintenance configuration "
                        "updated successfully."
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

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        kwargs['partial'] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# DELETE CONFIG (SOFT DELETE)
# =========================================================

class MaintenanceConfigDeleteAPIView(
    generics.DestroyAPIView
):

    queryset = (
        MaintenanceConfig.objects.all()
    )

    serializer_class = (
        MaintenanceConfigSerializer
    )

    lookup_field = 'pk'

    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        instance.is_active = False
        instance.save(
            update_fields=['is_active']
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance configuration "
                    "deactivated successfully."
                )
            },
            status=status.HTTP_200_OK
        )