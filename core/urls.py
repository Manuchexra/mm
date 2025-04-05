from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.courses.urls')),
    path('api/enrollments/', include('apps.enrollments.urls')),
]
