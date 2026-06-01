from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Complaint
from .serializers import ComplaintSerializer


# =========================================================
# CREATE COMPLAINT
# =========================================================

class ComplaintCreateAPIView(generics.CreateAPIView):

    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Complaint created successfully.",
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
# COMPLAINT LIST
# =========================================================

class ComplaintListAPIView(generics.ListAPIView):

    serializer_class = ComplaintSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        flat_id = self.request.GET.get(
            'flat_id',
            ''
        )

        user_id = self.request.GET.get(
            'user_id',
            ''
        )

        status_filter = self.request.GET.get(
            'status',
            ''
        )

        queryset = (
            Complaint.objects
            .select_related(
                'building',
                'flat',
                'user'
            )
            .order_by('-created_at')
        )

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(flat__flat_number__icontains=search)
            )

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
            )

        if flat_id:

            queryset = queryset.filter(
                flat_id=flat_id
            )

        if user_id:

            queryset = queryset.filter(
                user_id=user_id
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
                "message": "Complaint list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# COMPLAINT DETAILS
# =========================================================

class ComplaintDetailAPIView(generics.RetrieveAPIView):

    queryset = Complaint.objects.select_related(
        'building',
        'flat',
        'user'
    )

    serializer_class = ComplaintSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Complaint details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE COMPLAINT
# =========================================================

class ComplaintUpdateAPIView(generics.UpdateAPIView):

    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
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
                    "message": "Complaint updated successfully.",
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
# DELETE COMPLAINT
# =========================================================

class ComplaintDeleteAPIView(generics.DestroyAPIView):

    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Complaint deleted successfully."
            },
            status=status.HTTP_200_OK
        )