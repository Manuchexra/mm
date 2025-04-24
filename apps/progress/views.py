from rest_framework import generics
from .models import Progress
from .serializers import ProgressSerializer
from rest_framework.permissions import IsAuthenticated

class ProgressAPIView(generics.RetrieveAPIView):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        course_id = self.kwargs.get('course_id')
        progress, _ = Progress.objects.get_or_create(
            user=self.request.user,
            course_id=course_id
        )
        return progress