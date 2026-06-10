from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Flat
from .serializers import FlatSerializer


# =========================================================
# CREATE FLAT
# =========================================================

class FlatCreateAPIView(generics.CreateAPIView):

    queryset = Flat.objects.all()

    serializer_class = FlatSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Flat created successfully.",
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
# FLAT LIST
# =========================================================

class FlatListAPIView(generics.ListAPIView):

    serializer_class = FlatSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        wing_id = self.request.GET.get(
            'wing_id',
            ''
        )

        occupancy_status = self.request.GET.get(
            'occupancy_status',
            ''
        )

        is_active = self.request.GET.get(
            'is_active',
            ''
        )

        queryset = Flat.objects.select_related(
            'building',
            'wing',
            'owner'
        ).order_by(
            'wing__wing_name',
            'floor_number',
            'flat_number'
        )

        # =============================================
        # DEFAULT ACTIVE RECORDS
        # =============================================

        if is_active == '':

            queryset = queryset.filter(
                is_active=True
            )

        # =============================================
        # SEARCH
        # =============================================

        if search:

            queryset = queryset.filter(
                Q(flat_number__icontains=search) |
                Q(flat_type__icontains=search) |
                Q(occupancy_status__icontains=search) |
                Q(wing__wing_name__icontains=search) |
                Q(building__building_name__icontains=search)
            )

        # =============================================
        # BUILDING FILTER
        # =============================================

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
            )

        # =============================================
        # WING FILTER
        # =============================================

        if wing_id:

            queryset = queryset.filter(
                wing_id=wing_id
            )

        # =============================================
        # OCCUPANCY FILTER
        # =============================================

        if occupancy_status:

            queryset = queryset.filter(
                occupancy_status=occupancy_status
            )

        # =============================================
        # ACTIVE FILTER
        # =============================================

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

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Flat list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )



# =========================================================
# GET FLATS BY BUILDING ID
# =========================================================

class FlatByBuildingAPIView(generics.ListAPIView):

    serializer_class = FlatSerializer

    def get_queryset(self):

        building_id = self.kwargs.get('building_id')

        return Flat.objects.select_related(
            'building',
            'wing',
            'owner'
        ).filter(
            building_id=building_id,
            is_active=True
        ).order_by(
            'wing__wing_name',
            'floor_number',
            'flat_number'
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Flats fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

# =========================================================
# FLAT DETAILS
# =========================================================

class FlatDetailAPIView(generics.RetrieveAPIView):

    queryset = Flat.objects.select_related(
        'building',
        'wing',
        'owner'
    )

    serializer_class = FlatSerializer

    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Flat details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

# =========================================================
# UPDATE FLAT
# =========================================================

class FlatUpdateAPIView(generics.UpdateAPIView):

    queryset = Flat.objects.select_related(
        'building',
        'wing'
    )

    serializer_class = FlatSerializer

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
                    "message": "Flat updated successfully.",
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
# DEACTIVATE FLAT
# =========================================================

class FlatDeleteAPIView(generics.DestroyAPIView):

    queryset = Flat.objects.select_related(
        'building',
        'wing'
    )

    serializer_class = FlatSerializer

    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.is_active = False

        instance.save(
            update_fields=[
                'is_active',
                'updated_at'
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Flat deactivated successfully."
            },
            status=status.HTTP_200_OK
        )
    
from .models import FlatType
from .serializers import FlatTypeSerializer


# =========================================================
# CREATE FLAT TYPE
# =========================================================

class FlatTypeCreateAPIView(generics.CreateAPIView):

    queryset = FlatType.objects.all()

    serializer_class = FlatTypeSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Flat type created successfully.",
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
# FLAT TYPE LIST
# =========================================================

class FlatTypeListAPIView(generics.ListAPIView):

    serializer_class = FlatTypeSerializer

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

        queryset = FlatType.objects.select_related(
            'building'
        ).order_by(
            'name'
        )

        if is_active == '':

            queryset = queryset.filter(
                is_active=True
            )

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search)
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

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Flat type list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# GET FLAT TYPES BY BUILDING ID
# =========================================================

class FlatTypeByBuildingAPIView(generics.ListAPIView):

    serializer_class = FlatTypeSerializer

    def get_queryset(self):

        building_id = self.kwargs.get(
            'building_id'
        )

        return FlatType.objects.filter(
            building_id=building_id,
            is_active=True
        ).order_by(
            'name'
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Flat types fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# FLAT TYPE DETAILS
# =========================================================

class FlatTypeDetailAPIView(generics.RetrieveAPIView):

    queryset = FlatType.objects.select_related(
        'building'
    )

    serializer_class = FlatTypeSerializer

    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Flat type details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE FLAT TYPE
# =========================================================

class FlatTypeUpdateAPIView(generics.UpdateAPIView):

    queryset = FlatType.objects.select_related(
        'building'
    )

    serializer_class = FlatTypeSerializer

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
                    "message": "Flat type updated successfully.",
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
# DEACTIVATE FLAT TYPE
# =========================================================

class FlatTypeDeleteAPIView(generics.DestroyAPIView):

    queryset = FlatType.objects.select_related(
        'building'
    )

    serializer_class = FlatTypeSerializer

    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.is_active = False

        instance.save(
            update_fields=[
                'is_active',
                'updated_at'
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Flat type deactivated successfully."
            },
            status=status.HTTP_200_OK
        )
