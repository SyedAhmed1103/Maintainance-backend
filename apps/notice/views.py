from django.shortcuts import render

# Create your views here.
from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Notice
from .serializers import NoticeSerializer


# =========================================================
# CREATE NOTICE
# =========================================================

class NoticeCreateAPIView(generics.CreateAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Notice created successfully.",
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
# NOTICE LIST
# =========================================================

class NoticeListAPIView(generics.ListAPIView):

    serializer_class = NoticeSerializer

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

        queryset = Notice.objects.select_related(
            'building'
        ).order_by('-created_at')

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
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

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Notice list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# NOTICE DETAILS
# =========================================================

class NoticeDetailAPIView(generics.RetrieveAPIView):

    queryset = Notice.objects.select_related(
        'building'
    )

    serializer_class = NoticeSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "Notice details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE NOTICE
# =========================================================

class NoticeUpdateAPIView(generics.UpdateAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
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
                    "message": "Notice updated successfully.",
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
# DELETE NOTICE
# =========================================================

class NoticeDeleteAPIView(generics.DestroyAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "Notice deleted successfully."
            },
            status=status.HTTP_200_OK
        )