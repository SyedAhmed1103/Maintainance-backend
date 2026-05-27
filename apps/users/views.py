from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from .models import User

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UpdateUserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)


# ==========================================
# REGISTER API
# ==========================================

class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            email = serializer.validated_data['email']

            phone = serializer.validated_data['phone']

            password = serializer.validated_data['password']

            if User.objects.filter(email=email).exists():

                return Response(
                    {
                        'status': False,
                        'message': 'Email already exists'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(phone=phone).exists():

                return Response(
                    {
                        'status': False,
                        'message': 'Phone already exists'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create(

                first_name=serializer.validated_data['first_name'],

                last_name=serializer.validated_data.get(
                    'last_name'
                ),

                email=email,

                phone=phone,

                building_id=serializer.validated_data.get(
                    'building_id'
                ),

                user_type=serializer.validated_data.get(
                    'user_type'
                ),
            )

            user.password = make_password(password)

            user.save()

            return Response(
                {
                    'status': True,
                    'message': 'User registered successfully',
                    'data': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# LOGIN API
# ==========================================

class LoginView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            email = serializer.validated_data['email']

            password = serializer.validated_data['password']

            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:

                return Response(
                    {
                        'status': False,
                        'message': 'Invalid email'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not check_password(password, user.password):

                return Response(
                    {
                        'status': False,
                        'message': 'Invalid password'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'status': True,
                    'message': 'Login successful',
                    'data': UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# USER LIST API
# ==========================================

class UserListView(GenericAPIView):

    serializer_class = UserSerializer

    def get(self, request):

        users = User.objects.all().order_by('-id')

        serializer = self.get_serializer(
            users,
            many=True
        )

        return Response(
            {
                'status': True,
                'count': users.count(),
                'data': serializer.data
            }
        )


# ==========================================
# USER DETAIL API
# ==========================================

class UserDetailView(GenericAPIView):

    serializer_class = UserSerializer

    def get_object(self, id):

        try:
            return User.objects.get(id=id)

        except User.DoesNotExist:
            return None

    def get(self, request, id):

        user = self.get_object(id)

        if not user:

            return Response(
                {
                    'status': False,
                    'message': 'User not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(user)

        return Response(
            {
                'status': True,
                'data': serializer.data
            }
        )


# ==========================================
# UPDATE USER API
# ==========================================

class UpdateUserView(GenericAPIView):

    serializer_class = UpdateUserSerializer

    def get_object(self, id):

        try:
            return User.objects.get(id=id)

        except User.DoesNotExist:
            return None

    def put(self, request, id):

        user = self.get_object(id)

        if not user:

            return Response(
                {
                    'status': False,
                    'message': 'User not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    'status': True,
                    'message': 'User updated successfully',
                    'data': serializer.data
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# DELETE USER API
# ==========================================

class DeleteUserView(GenericAPIView):

    def delete(self, request, id):

        try:

            user = User.objects.get(id=id)

        except User.DoesNotExist:

            return Response(
                {
                    'status': False,
                    'message': 'User not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response(
            {
                'status': True,
                'message': 'User deleted successfully'
            }
        )


# ==========================================
# FORGOT PASSWORD API
# ==========================================

class ForgotPasswordView(GenericAPIView):

    serializer_class = ForgotPasswordSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )
 
        if serializer.is_valid():

            email = serializer.validated_data['email']

            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:

                return Response(
                    {
                        'status': False,
                        'message': 'Email not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            reset_token = get_random_string(50)

            user.reset_token = reset_token

            user.save()

            reset_link = (
                f"http://127.0.0.1:8000/api/users/reset-password/"
                f"{reset_token}"
            )

            send_mail(
                subject='Reset Password',
                message=f'Click here: {reset_link}',
                from_email='inquiry@itdax.in',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {
                    'status': True,
                    'message': 'Reset password link sent'
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# RESET PASSWORD API
# ==========================================

class ResetPasswordView(GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():

            token = serializer.validated_data['token']

            password = serializer.validated_data['password']

            try:

                user = User.objects.get(
                    reset_token=token
                )

            except User.DoesNotExist:

                return Response(
                    {
                        'status': False,
                        'message': 'Invalid token'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.password = make_password(password)

            user.reset_token = None

            user.save()

            return Response(
                {
                    'status': True,
                    'message': 'Password reset successful'
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )