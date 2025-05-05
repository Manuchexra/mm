from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import SearchHistory, FilterOptions
from apps.courses.models import Course
from apps.mentors.models import Mentor
from .serializers import SearchResultSerializer, FilteredSearchSerializer

# Search endpoint with Swagger documentation
@swagger_auto_schema(
    method='get',
    operation_description="Search across courses and mentors",
    manual_parameters=[
        openapi.Parameter(
            'q',
            openapi.IN_QUERY,
            description="Search query string (e.g. python, mentor)",
            type=openapi.TYPE_STRING
        ),
    ],
    responses={
        200: openapi.Response(
            description="Successful search results",
            schema=SearchResultSerializer
        ),
        400: openapi.Response(
            description="Bad request when query is empty",
            examples={
                "application/json": {
                    "error": "Search query is empty"
                }
            }
        )
    }
)
@api_view(['GET'])
def search(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({'error': 'Search query is empty'}, status=400)

    courses = Course.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    mentors = Mentor.objects.filter(
        Q(user__username__icontains=query)
    )

    if request.user.is_authenticated:
        SearchHistory.objects.create(query=query, user=request.user)

    serializer = SearchResultSerializer({
        'courses': courses,
        'mentors': mentors
    }, context={'request': request})

    return Response(serializer.data)

# Search with filters endpoint with Swagger documentation
@swagger_auto_schema(
    method='get',
    operation_description="Search with advanced filters",
    manual_parameters=[
        openapi.Parameter(
            'q',
            openapi.IN_QUERY,
            description="Search query string",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'category',
            openapi.IN_QUERY,
            description="Filter by category slug",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'min_price',
            openapi.IN_QUERY,
            description="Minimum price filter",
            type=openapi.TYPE_NUMBER,
            required=False
        ),
        openapi.Parameter(
            'max_price',
            openapi.IN_QUERY,
            description="Maximum price filter",
            type=openapi.TYPE_NUMBER,
            required=False
        ),
        openapi.Parameter(
            'rating',
            openapi.IN_QUERY,
            description="Minimum rating filter",
            type=openapi.TYPE_NUMBER,
            required=False
        ),
        openapi.Parameter(
            'is_free',
            openapi.IN_QUERY,
            description="Filter free courses (true/false)",
            type=openapi.TYPE_BOOLEAN,
            required=False
        ),
    ],
    responses={
        200: openapi.Response(
            description="Successful filtered search results",
            schema=FilteredSearchSerializer
        ),
        400: openapi.Response(
            description="Bad request when invalid parameters provided",
            examples={
                "application/json": {
                    "error": "Invalid price range"
                }
            }
        )
    }
)
@api_view(['GET'])
def search_with_filters(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    is_free = request.GET.get('is_free')

    # Validate price range
    if min_price and max_price and float(min_price) > float(max_price):
        return Response({'error': 'Invalid price range'}, status=400)

    # Build filters for courses
    course_filters = Q()
    if query:
        course_filters &= (Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        course_filters &= Q(category__slug=category)
    if min_price:
        course_filters &= Q(price__gte=float(min_price))
    if max_price:
        course_filters &= Q(price__lte=float(max_price))
    if rating:
        course_filters &= Q(rating__gte=float(rating))
    if is_free:
        if is_free.lower() == 'true':
            course_filters &= Q(price=0)

    # Build filters for mentors
    mentor_filters = Q()
    if query:
        mentor_filters &= Q(user__username__icontains=query)

    # Apply filters
    courses = Course.objects.filter(course_filters)
    mentors = Mentor.objects.filter(mentor_filters)
    all_filter_options = FilterOptions.objects.all()

    # Prepare applied filters for response
    applied_filters = {
        'query': query or None,
        'category': category,
        'min_price': float(min_price) if min_price else None,
        'max_price': float(max_price) if max_price else None,
        'rating': float(rating) if rating else None,
        'is_free': is_free.lower() == 'true' if is_free else None
    }

    # Remove None values from applied filters
    applied_filters = {k: v for k, v in applied_filters.items() if v is not None}

    serializer = FilteredSearchSerializer({
        'courses': courses,
        'mentors': mentors,
        'filters': all_filter_options,
        'applied_filters': applied_filters
    }, context={'request': request})

    return Response(serializer.data)