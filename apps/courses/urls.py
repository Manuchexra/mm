from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CourseViewSet, CategoryViewSet, SectionViewSet, LessonViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('categories', CategoryViewSet, basename='category')
router.register('sections', SectionViewSet, basename='section')
router.register('lessons', LessonViewSet, basename='lesson')


urlpatterns = [
    path('', include(router.urls)),
]
