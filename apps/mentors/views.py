from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Mentor
from apps.courses.serializers import CourseSerializer  # apps.courses.serializers dan import qilish kerak
from .serializers import MentorSerializer
from apps.users.models import User

class MentorListView(generics.ListCreateAPIView):
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get_queryset(self):
        queryset = Mentor.objects.select_related('user').all()
        
        # Filtrlash parametrlari
        expertise = self.request.query_params.get('expertise')
        search = self.request.query_params.get('search')
        
        if expertise:
            queryset = queryset.filter(expertise=expertise)
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(bio__icontains=search)
            )
        return queryset
    
    def perform_create(self, serializer):
        # Faqat admin yoki superuser yangi mentor yaratishi mumkin
        if not self.request.user.is_staff:
            return Response(
                {"detail": "Faqat adminlar yangi mentor qo'sha oladi"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = self.request.data.get('user_id')
        if not user_id:
            return Response(
                {"user_id": "Bu maydon to'ldirilishi shart"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = get_object_or_404(User, pk=user_id)
        serializer.save(user=user)

class MentorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.select_related('user')
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class TopMentorListView(generics.ListAPIView):
    serializer_class = MentorSerializer
    permission_classes = [permissions.AllowAny]  # Top mentorlar hamma uchun ochiq
    
    def get_queryset(self):
        return Mentor.objects.filter(
            is_top_mentor=True
        ).select_related('user').order_by('-rating')

class MentorCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer  # apps.courses.serializers dan import qilish kerak
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        mentor = get_object_or_404(Mentor, pk=self.kwargs['pk'])
        return mentor.courses.filter(is_published=True)