# apps/complaint/views.py

from django.db import transaction
from django.utils import timezone

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from .models import Complaint
from .serializers import ComplaintSerializer

from apps.media_manager.models import Media
from apps.media_manager.services import MediaService


class ComplaintListAPIView(
    generics.ListAPIView
):

    serializer_class = ComplaintSerializer

    def get_queryset(self):

        queryset = (
            Complaint.objects
            .filter(
                is_deleted=False
            )
            .select_related(
                "building",
                "flat",
                "user",
            )
            .order_by(
                "-created_at"
            )
        )

        building_id = (
            self.request.query_params.get(
                "building_id"
            )
        )

        flat_id = (
            self.request.query_params.get(
                "flat_id"
            )
        )

        user_id = (
            self.request.query_params.get(
                "user_id"
            )
        )

        complaint_status = (
            self.request.query_params.get(
                "status"
            )
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

        if complaint_status:
            queryset = queryset.filter(
                status=complaint_status
            )

        return queryset


class ComplaintCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = ComplaintSerializer

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = self.get_serializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        complaint = serializer.save()

        uploaded_images = (
            request.FILES.getlist(
                "images"
            )
        )

        if uploaded_images:

            MediaService.upload_multiple(
                instance=complaint,
                files=uploaded_images,
                category=(
                    Media.Category
                    .COMPLAINT_ATTACHMENT
                ),
            )

        response_serializer = (
            ComplaintSerializer(
                complaint,
                context={
                    "request": request
                }
            )
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Complaint created successfully."
                ),
                "data": (
                    response_serializer.data
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class ComplaintDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = ComplaintSerializer

    lookup_field = "pk"

    def get_queryset(self):

        return (
            Complaint.objects
            .filter(
                is_deleted=False
            )
            .select_related(
                "building",
                "flat",
                "user",
            )
        )


class ComplaintUpdateAPIView(
    generics.UpdateAPIView
):

    serializer_class = ComplaintSerializer

    lookup_field = "pk"

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def get_queryset(self):

        return (
            Complaint.objects
            .filter(
                is_deleted=False
            )
        )

    @transaction.atomic
    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        partial = kwargs.pop(
            "partial",
            False
        )

        complaint = self.get_object()

        serializer = self.get_serializer(
            complaint,
            data=request.data,
            partial=partial,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        complaint = serializer.save()

        uploaded_images = (
            request.FILES.getlist(
                "images"
            )
        )

        if uploaded_images:

            MediaService.delete_single_by_category(
                instance=complaint,
                category=(
                    Media.Category
                    .COMPLAINT_ATTACHMENT
                ),
            )

            MediaService.upload_multiple(
                instance=complaint,
                files=uploaded_images,
                category=(
                    Media.Category
                    .COMPLAINT_ATTACHMENT
                ),
            )

        response_serializer = (
            ComplaintSerializer(
                complaint,
                context={
                    "request": request
                }
            )
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Complaint updated successfully."
                ),
                "data": (
                    response_serializer.data
                ),
            },
            status=status.HTTP_200_OK,
        )


class ComplaintDeleteAPIView(
    generics.DestroyAPIView
):

    serializer_class = ComplaintSerializer

    lookup_field = "pk"

    def get_queryset(self):

        return (
            Complaint.objects
            .filter(
                is_deleted=False
            )
        )

    @transaction.atomic
    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        complaint = self.get_object()

        complaint.is_deleted = True

        complaint.deleted_at = (
            timezone.now()
        )

        complaint.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Complaint deleted successfully."
                ),
            },
            status=status.HTTP_200_OK,
        )