from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    
    path('api/buildings/', include('apps.building.urls')),
    path('api/wings/', include('apps.wing.urls')),
    path('api/flats/', include('apps.flats.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/admin/', include('apps.admins.urls')),
    path('api/income/', include('apps.income.urls')),
    path('api/complaint/', include('apps.complaint.urls')),
    path('api/notice/', include('apps.notice.urls')),
    path('api/expense/', include('apps.expense.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),

]
