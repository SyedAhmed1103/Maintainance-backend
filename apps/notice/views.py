from rest_framework import generics, status
from rest_framework.response import Response

from .models import Notice
from .serializers import NoticeSerializer

from apps.media_manager.models import Media
from apps.media_manager.services import MediaService


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

        serializer.is_valid(
            raise_exception=True
        )

        notice = serializer.save()

        attachment = request.FILES.get(
            "attachment"
        )

        if attachment:

            MediaService.upload_single(
                instance=notice,
                file=attachment,
                category=Media.Category.NOTICE_ATTACHMENT,
                media_type=Media.MediaType.DOCUMENT,
            )

        return Response(
            {
                "success": True,
                "message": "Notice created successfully.",
                "data": NoticeSerializer(
                    notice
                ).data
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# NOTICE LIST
# =========================================================

class NoticeListAPIView(
    generics.ListAPIView
):

    serializer_class = NoticeSerializer

    def get_queryset(self):

        return (
            Notice.objects
            .filter(
                is_active=True
            )
            .select_related(
                "building",
                "created_by"
            )
            .order_by(
                "-created_at"
            )
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
                "message": "Notices fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# BUILDING NOTICE LIST
# =========================================================

class BuildingNoticeListAPIView(
    generics.ListAPIView
):

    serializer_class = NoticeSerializer

    def get_queryset(self):

        building_id = self.kwargs.get(
            "building_id"
        )

        return (
            Notice.objects
            .filter(
                building_id=building_id,
                is_active=True
            )
            .select_related(
                "building",
                "created_by"
            )
            .order_by(
                "-created_at"
            )
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
                "message": "Building notices fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# NOTICE DETAIL
# =========================================================

class NoticeDetailAPIView(
    generics.RetrieveAPIView
):

    queryset = (
        Notice.objects
        .select_related(
            "building",
            "created_by"
        )
    )

    serializer_class = NoticeSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):

        notice = self.get_object()

        serializer = self.get_serializer(
            notice
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

class NoticeUpdateAPIView(
    generics.UpdateAPIView
):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop(
            "partial",
            False
        )

        notice = self.get_object()

        serializer = self.get_serializer(
            notice,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        notice = serializer.save()

        attachment = request.FILES.get(
            "attachment"
        )

        if attachment:

            MediaService.replace_single(
                instance=notice,
                file=attachment,
                category=Media.Category.NOTICE_ATTACHMENT,
                media_type=Media.MediaType.DOCUMENT,
            )

        return Response(
            {
                "success": True,
                "message": "Notice updated successfully.",
                "data": NoticeSerializer(
                    notice
                ).data
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


# =========================================================
# SOFT DELETE NOTICE
# =========================================================

class NoticeDeleteAPIView(
    generics.UpdateAPIView
):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):

        notice = self.get_object()

        notice.is_active = False

        notice.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Notice deleted successfully."
            },
            status=status.HTTP_200_OK
        )