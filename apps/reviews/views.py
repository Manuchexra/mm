from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        if course_id:
            return Review.objects.filter(course__id=course_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
