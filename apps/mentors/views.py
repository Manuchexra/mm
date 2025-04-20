# views.py faylida
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from .models import Mentor
from .serializers import MentorSerializer

class MentorListView(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MentorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]  # Fayl yuklash uchun

class TopMentorListView(generics.ListAPIView):
    queryset = Mentor.objects.filter(is_top_mentor=True)
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]