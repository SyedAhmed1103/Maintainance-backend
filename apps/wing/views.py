from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Wing
from .serializers import WingSerializer


# =========================================================
# CREATE WING
# =========================================================

class WingCreateAPIView(generics.CreateAPIView):

    queryset = Wing.objects.all()
    serializer_class = WingSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Wing created successfully.",
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
# WING LIST
# =========================================================

class WingListAPIView(generics.ListAPIView):

    serializer_class = WingSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        queryset = Wing.objects.select_related(
            'building'
        ).filter(
            is_active=True
        ).order_by('-id')

        if search:

            queryset = queryset.filter(
                Q(wing_name__icontains=search) |
                Q(building__building_name__icontains=search)
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
                "message": "Wing list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# GET WINGS BY BUILDING ID
# =========================================================

class WingByBuildingAPIView(generics.ListAPIView):

    serializer_class = WingSerializer

    def get_queryset(self):

        building_id = self.kwargs.get('building_id')

        return Wing.objects.filter(
            building_id=building_id,
            is_active=True
        ).select_related('building').order_by('wing_name')

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Wings fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

# =========================================================
# WING DETAILS
# =========================================================

class WingDetailAPIView(generics.RetrieveAPIView):

    queryset = Wing.objects.select_related(
        'building'
    )

    serializer_class = WingSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Wing details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE WING
# =========================================================

class WingUpdateAPIView(generics.UpdateAPIView):

    queryset = Wing.objects.all()
    serializer_class = WingSerializer
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
                    "message": "Wing updated successfully.",
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
# DEACTIVATE WING
# =========================================================

class WingDeleteAPIView(generics.DestroyAPIView):

    queryset = Wing.objects.all()
    serializer_class = WingSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(
            {
                "success": True,
                "message": "Wing deactivated successfully."
            },
            status=status.HTTP_200_OK
        )