from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer


# =========================================================
# CREATE USER
# =========================================================

class UserCreateAPIView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            password = request.data.get(
                'password'
            )

            if password:

                user.set_password(password)
                user.save()

            return Response(
                {
                    "success": True,
                    "message": "User created successfully.",
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
# USER LIST
# =========================================================

class UserListAPIView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):

        search = self.request.GET.get(
            'search',
            ''
        )

        user_type = self.request.GET.get(
            'user_type',
            ''
        )

        building_id = self.request.GET.get(
            'building_id',
            ''
        )

        is_verified = self.request.GET.get(
            'is_verified',
            ''
        )

        queryset = User.objects.select_related(
            'building',
            'flat'
        ).order_by('-id')

        if search:

            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(mobile__icontains=search)
            )

        if user_type:

            queryset = queryset.filter(
                user_type=user_type
            )

        if building_id:

            queryset = queryset.filter(
                building_id=building_id
            )

        if is_verified != '':

            if is_verified.lower() == 'true':

                queryset = queryset.filter(
                    is_verified=True
                )

            elif is_verified.lower() == 'false':

                queryset = queryset.filter(
                    is_verified=False
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
                "message": "User list fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# USER DETAILS
# =========================================================

class UserDetailAPIView(generics.RetrieveAPIView):

    queryset = User.objects.select_related(
        'building',
        'flat'
    )

    serializer_class = UserSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response(
            {
                "success": True,
                "message": "User details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE USER
# =========================================================

class UserUpdateAPIView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
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

            user = serializer.save()

            password = request.data.get(
                'password'
            )

            if password:

                user.set_password(password)
                user.save()

            return Response(
                {
                    "success": True,
                    "message": "User updated successfully.",
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
# DELETE USER
# =========================================================

class UserDeleteAPIView(generics.DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "success": True,
                "message": "User deleted successfully."
            },
            status=status.HTTP_200_OK
        )