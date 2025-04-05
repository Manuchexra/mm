from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import Enrollment, LessonProgress
from apps.courses.models import Course, Lesson
from .serializers import (
    EnrollmentSerializer,
    LessonProgressSerializer,
    CompleteLessonSerializer
)


class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        if not course_id:
            return Response({"error": "course ID kerak"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Bunday kurs mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
        
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

        if not created:
            return Response({"message": "Siz allaqachon ushbu kursga yozilgansiz."})

        # Auto-create LessonProgress for all lessons
        lessons = Lesson.objects.filter(section__course=course)
        LessonProgress.objects.bulk_create([
            LessonProgress(enrollment=enrollment, lesson=lesson) for lesson in lessons
        ])

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)


class MyCourseProgressView(generics.ListAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return LessonProgress.objects.filter(
            enrollment__user=self.request.user,
            enrollment__course__id=course_id
        )


class CompleteLessonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        serializer = CompleteLessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson_id = serializer.validated_data['lesson_id']

        try:
            enrollment = Enrollment.objects.get(user=request.user, course__id=course_id)
        except Enrollment.DoesNotExist:
            return Response({"error": "Siz bu kursga yozilmagansiz."}, status=403)

        try:
            progress = LessonProgress.objects.get(enrollment=enrollment, lesson__id=lesson_id)
        except LessonProgress.DoesNotExist:
            return Response({"error": "Dars topilmadi."}, status=404)

        progress.completed = True
        progress.completed_at = now()
        progress.save()

        return Response({"message": "Dars muvaffaqiyatli yakunlandi."})
