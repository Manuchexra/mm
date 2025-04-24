from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course, Category, Section, Lesson
from .serializers import (
    CourseSerializer,
    CourseCreateSerializer,
    CategorySerializer,
    SectionSerializer,
    LessonSerializer
)


from rest_framework import viewsets, parsers

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

# apps/courses/views.py
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Count
from .models import Course
from .serializers import CourseSerializer

# Agar ViewSet ishlatayotgan bo'lsangiz:
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=['GET'])
    def popular(self, request):
        popular_courses = Course.objects.annotate(
            enrollments_count=Count('enrollments')
        ).order_by('-enrollments_count')[:5]
        serializer = self.get_serializer(popular_courses, many=True)
        return Response(serializer.data)

# Yoki alohida funksiya sifatida:
@api_view(['GET'])
def popular_courses(request):
    popular_courses = Course.objects.annotate(
        enrollments_count=Count('enrollments')
    ).order_by('-enrollments_count')[:5]
    serializer = CourseSerializer(popular_courses, many=True)
    return Response(serializer.data)



