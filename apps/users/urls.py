from django.urls import path

from .views import (

    RegisterView,
    LoginView,

    UserListView,
    UserDetailView,
    UpdateUserView,
    DeleteUserView,

    ForgotPasswordView,
    ResetPasswordView,
)


urlpatterns = [

    # ==========================================
    # AUTH APIs
    # ==========================================

    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),

    path(
        'forgot-password/',
        ForgotPasswordView.as_view(),
        name='forgot-password'
    ),

    path(
        'reset-password/',
        ResetPasswordView.as_view(),
        name='reset-password'
    ),


    # ==========================================
    # USER CRUD APIs
    # ==========================================

    path(
        '',
        UserListView.as_view(),
        name='user-list'
    ),

    path(
        '<int:id>/',
        UserDetailView.as_view(),
        name='user-detail'
    ),

    path(
        'update/<int:id>/',
        UpdateUserView.as_view(),
        name='update-user'
    ),

    path(
        'delete/<int:id>/',
        DeleteUserView.as_view(),
        name='delete-user'
    ),
]