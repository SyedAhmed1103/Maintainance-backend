from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Admin
from .serializers import AdminSerializer


# =========================================================
# CREATE ADMIN
# =========================================================

class AdminCreateAPIView(generics.CreateAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Admin created successfully.",
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
# ADMIN LIST
# =========================================================

class AdminListAPIView(generics.ListAPIView):

    serializer_class = AdminSerializer

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

        queryset = Admin.objects.select_related(
            'building'
        ).order_by('-id')

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(mobile__icontains=search) |
                Q(building__building_name__icontains=search)
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
                "message": "Admin list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# ADMIN DETAILS
# =========================================================

class AdminDetailAPIView(generics.RetrieveAPIView):

    queryset = Admin.objects.select_related(
        'building'
    )

    serializer_class = AdminSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Admin details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE ADMIN
# =========================================================

class AdminUpdateAPIView(generics.UpdateAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
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
                    "message": "Admin updated successfully.",
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
# DELETE ADMIN
# =========================================================

class AdminDeleteAPIView(generics.DestroyAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Admin deleted successfully."
            },
            status=status.HTTP_200_OK
        )