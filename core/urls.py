from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
   openapi.Info(
      title="Online Course API",
      default_version='v1',
      description="Online Course platformasi uchun REST API hujjatlari",
      terms_of_service="https://yourdomain.com/terms/",
      contact=openapi.Contact(email="support@yourdomain.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # === API Apps ===
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.courses.urls')),
    path('api/enrollments/', include('apps.enrollments.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/wishlist/', include('apps.wishlist.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]


# === Swagger & Redoc Docs ===
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
