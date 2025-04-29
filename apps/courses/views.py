from rest_framework import viewsets, permissions
from rest_framework import viewsets, permissions, parsers
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # Bu qatorni qo'shing
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Course, Category, Section, Lesson
from .serializers import (
    CourseSerializer,
    CourseCreateSerializer,
    CategorySerializer,
    SectionSerializer,
    LessonSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=False, methods=['GET'])
    def popular(self, request):
        """Get 5 most popular courses by enrollment count"""
        popular_courses = Course.objects.annotate(
            enrollments_count=Count('enrollments')
        ).order_by('-enrollments_count')[:5]
        serializer = self.get_serializer(popular_courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='category/(?P<category_id>[0-9]+)')
    def by_category_id(self, request, category_id=None):
        """Get courses by category ID"""
        try:
            category_id = int(category_id)
            category = get_object_or_404(Category, id=category_id)
            courses = self.queryset.filter(category=category)
            serializer = self.get_serializer(courses, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid category ID"}, status=400)

    @action(detail=False, methods=['GET'], url_path='slug/(?P<category_slug>[-\w]+)')
    def by_category_slug(self, request, category_slug=None):
        """Get courses by category slug"""
        category = get_object_or_404(Category, slug=category_slug)
        courses = self.queryset.filter(category=category)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]