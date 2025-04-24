from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EnrollView,
    MyEnrollmentsView,
    MyCourseProgressView,
    CompleteLessonView,
    EnrollmentViewSet
)

router = DefaultRouter()
router.register('', EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    # Avtomatik ViewSet marshrutlari
    path('', include(router.urls)),
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('my/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('progress/<int:course_id>/', MyCourseProgressView.as_view(), name='course-progress'),
    path('complete/<int:course_id>/', CompleteLessonView.as_view(), name='complete-lesson'),
]

from rest_framework.authtoken import views as drf_auth_views

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),  # browsable login form
]
