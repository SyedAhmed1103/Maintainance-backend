from django.db import transaction
from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

from apps.flats.models import Flat

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

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Validation error.",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        flat_ids = request.data.get(
            'flat_ids',
            []
        )

        flats = Flat.objects.filter(
            id__in=flat_ids,
            is_active=True
        )

        if len(flat_ids) != flats.count():

            return Response(
                {
                    "success": False,
                    "message":
                    "One or more flats are invalid."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        building = serializer.validated_data.get(
            'building'
        )

        for flat in flats:

            if flat.building_id != building.id:

                return Response(
                    {
                        "success": False,
                        "message":
                        f"Flat {flat.flat_number} does not belong to selected building."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if flat.owner:

                return Response(
                    {
                        "success": False,
                        "message":
                        f"Flat {flat.flat_number} already has an owner."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        with transaction.atomic():

            user = serializer.save()

            password = request.data.get(
                'password'
            )

            if password:

                user.set_password(
                    password
                )

                user.save()

            for flat in flats:

                flat.owner = user

                flat.occupancy_status = (
                    'occupied'
                )

                flat.save()

        return Response(
            {
                "success": True,
                "message":
                "User created successfully.",
                "data":
                UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
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

        is_active = self.request.GET.get(
            'is_active',
            ''
        )

        queryset = (
            User.objects
            .select_related(
                'building'
            )
            .prefetch_related(
                'flats',
                'flats__wing'
            )
            .order_by('-id')
        )

        if is_active == '':

            queryset = queryset.filter(
                is_active=True
            )

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
                "message":
                "User list fetched successfully.",
                "count":
                queryset.count(),
                "data":
                serializer.data
            },
            status=status.HTTP_200_OK
        )

# =========================================================

# USER DETAILS

# =========================================================

class UserDetailAPIView(generics.RetrieveAPIView):

    queryset = (
        User.objects
        .select_related(
            'building'
        )
        .prefetch_related(
            'flats',
            'flats__wing'
        )
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
                "message":
                "User details fetched successfully.",
                "data":
                serializer.data
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

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message":
                    "Validation error.",
                    "errors":
                    serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        flat_ids = request.data.get(
            'flat_ids',
            []
        )

        flats = Flat.objects.filter(
            id__in=flat_ids,
            is_active=True
        )

        if flat_ids:

            if len(flat_ids) != flats.count():

                return Response(
                    {
                        "success": False,
                        "message":
                        "One or more flats are invalid."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            building = serializer.validated_data.get(
                'building',
                instance.building
            )

            for flat in flats:

                if flat.building_id != building.id:

                    return Response(
                        {
                            "success": False,
                            "message":
                            f"Flat {flat.flat_number} does not belong to selected building."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if (
                    flat.owner
                    and flat.owner != instance
                ):

                    return Response(
                        {
                            "success": False,
                            "message":
                            f"Flat {flat.flat_number} already has an owner."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        with transaction.atomic():

            user = serializer.save()

            password = request.data.get(
                'password'
            )

            if password:

                user.set_password(
                    password
                )

                user.save()

            if flat_ids:

                Flat.objects.filter(
                    owner=user
                ).exclude(
                    id__in=flat_ids
                ).update(
                    owner=None
                )

                for flat in flats:

                    flat.owner = user

                    flat.occupancy_status = (
                        'occupied'
                    )

                    flat.save()

        return Response(
            {
                "success": True,
                "message":
                "User updated successfully.",
                "data":
                UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        kwargs['partial'] = True

        return self.update(
            request,
            *args,
            **kwargs
        )

# =========================================================

# DEACTIVATE USER

# =========================================================

class UserDeleteAPIView(generics.DestroyAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        with transaction.atomic():

            Flat.objects.filter(
                owner=instance
            ).update(
                owner=None
            )

            instance.is_active = False

            instance.save()

        return Response(
            {
                "success": True,
                "message":
                "User deactivated successfully."
            },
            status=status.HTTP_200_OK
        )
