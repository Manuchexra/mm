from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from .serializers import SearchResultSerializer
from .models import SearchHistory
from apps.courses.models import Course
from apps.mentors.models import Mentor

# Swagger uchun importlar:
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger query parametri
query_param = openapi.Parameter(
    'q', openapi.IN_QUERY,
    description="Search query string (e.g. python, mentor)",
    type=openapi.TYPE_STRING
)

@swagger_auto_schema(method='get', manual_parameters=[query_param])
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
    }, context={'request': request})  # Pass request to serializer

    return Response(serializer.data)