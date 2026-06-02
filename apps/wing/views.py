from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Wing
from .serializers import WingSerializer


class WingCreateAPIView(GenericAPIView):
    serializer_class = WingSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Wing created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class WingListAPIView(GenericAPIView):
    serializer_class = WingSerializer

    def get(self, request):
        wings = Wing.objects.all().order_by('-id')

        serializer = self.serializer_class(
            wings,
            many=True
        )

        return Response(
            {
                "message": "Wing list fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class WingDetailAPIView(GenericAPIView):
    serializer_class = WingSerializer

    def get(self, request, pk):
        try:
            wing = Wing.objects.get(id=pk)

        except Wing.DoesNotExist:
            return Response(
                {
                    "message": "Wing not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(wing)

        return Response(
            {
                "message": "Wing details fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class WingUpdateAPIView(GenericAPIView):
    serializer_class = WingSerializer

    def put(self, request, pk):
        try:
            wing = Wing.objects.get(id=pk)

        except Wing.DoesNotExist:
            return Response(
                {
                    "message": "Wing not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            wing,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Wing updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class WingDeleteAPIView(GenericAPIView):

    def delete(self, request, pk):
        try:
            wing = Wing.objects.get(id=pk)

        except Wing.DoesNotExist:
            return Response(
                {
                    "message": "Wing not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        wing.delete()

        return Response(
            {
                "message": "Wing deleted successfully"
            },
            status=status.HTTP_200_OK
        )