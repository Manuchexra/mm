# mentors/views.py
from rest_framework import generics, permissions
from .models import Mentor
from .serializers import MentorSerializer

class MentorListView(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MentorDetailView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TopMentorListView(generics.ListAPIView):
    queryset = Mentor.objects.filter(is_top_mentor=True)
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]