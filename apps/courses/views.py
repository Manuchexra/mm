from rest_framework import viewsets, permissions, parsers, status
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from apps.wishlist.models import Wishlist
from .models import Course, Category, Section, Lesson
from .serializers import (
    CourseSerializer,
    CourseCreateSerializer,
    CategorySerializer,
    SectionSerializer,
    LessonSerializer
)
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('category', 'instructor')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        methods=['DELETE'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="Course ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: 'Wishlist status changed successfully',
            400: 'Bad request',
            401: 'Unauthorized'
        }
    )
    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def wishlist(self, request, pk=None):
        """
        Remove course from user's wishlist (DELETE only)
        """
        course = self.get_object()
        deleted, _ = Wishlist.objects.filter(
            user=request.user,
            course=course
        ).delete()
        if deleted:
            return Response({'status': 'removed from wishlist'}, status=status.HTTP_200_OK)
        return Response({'status': 'not in wishlist'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        responses={200: CourseSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="A search term",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of results per page",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'offset',
                openapi.IN_QUERY,
                description="Initial index for pagination",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ]
    )
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_wishlist(self, request):
        """
        Get current user's wishlist with optional filtering
        """
        queryset = Course.objects.filter(
            wishlisted_by__user=request.user
        ).order_by('-wishlisted_by__created_at')
        
        # Category filter
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
            
        # Search filter
        search_term = request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | 
                Q(description__icontains=search_term)
            )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Category filter
        if 'category_id' in self.request.GET:
            queryset = queryset.filter(category__id=self.request.GET['category_id'])
            
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of results per page",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'offset',
                openapi.IN_QUERY,
                description="Initial index for pagination",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Get list of courses with optional filtering and pagination
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of results per page",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'offset',
                openapi.IN_QUERY,
                description="Initial index for pagination",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    @action(detail=False, methods=['GET'])
    def popular(self, request):
        """
        Get popular courses ordered by enrollment count
        """
        queryset = self.get_queryset().annotate(
            enrollments_count=Count('enrollments')
        ).order_by('-enrollments_count')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
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