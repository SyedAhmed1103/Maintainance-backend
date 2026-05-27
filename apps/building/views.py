from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Building
from .serializers import BuildingSerializer


# =========================================================
# CREATE BUILDING
# =========================================================

class BuildingCreateAPIView(generics.CreateAPIView):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                created_by=request.user
                if request.user.is_authenticated
                else None
            )

            return Response(
                {
                    "success": True,
                    "message": "Building created successfully.",
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
# BUILDING LIST
# =========================================================

class BuildingListAPIView(generics.ListAPIView):

    serializer_class = BuildingSerializer

    def get_queryset(self):

        search = self.request.GET.get('search', '')
        building_type = self.request.GET.get(
            'building_type',
            ''
        )
        is_active = self.request.GET.get(
            'is_active',
            ''
        )

        queryset = Building.objects.all().order_by('-id')

        # =================================================
        # SEARCH FILTER
        # =================================================

        if search:

            queryset = queryset.filter(
                Q(building_name__icontains=search) |
                Q(building_code__icontains=search) |
                Q(city__icontains=search) |
                Q(state__icontains=search)
            )

        # =================================================
        # BUILDING TYPE FILTER
        # =================================================

        if building_type:

            queryset = queryset.filter(
                building_type=building_type
            )

        # =================================================
        # ACTIVE FILTER
        # =================================================

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
                "message": "Building list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# BUILDING DETAILS
# =========================================================

class BuildingDetailAPIView(generics.RetrieveAPIView):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response(
            {
                "success": True,
                "message": "Building details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE BUILDING
# =========================================================

class BuildingUpdateAPIView(generics.UpdateAPIView):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)

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
                    "message": "Building updated successfully.",
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

    # PATCH SUPPORT

    def patch(self, request, *args, **kwargs):

        kwargs['partial'] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# DELETE BUILDING
# =========================================================

class BuildingDeleteAPIView(generics.DestroyAPIView):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Building deleted successfully."
            },
            status=status.HTTP_200_OK
        )