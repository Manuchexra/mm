from rest_framework import serializers
from apps.courses.models import Course, Lesson
from .models import Enrollment, LessonProgress


# === 1. LessonProgress Serializer ===
class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.ReadOnlyField(source='lesson.title')

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'lesson_title', 'completed', 'completed_at']


# === 2. Enrollment Serializer ===
class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    enrolled_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_title', 'enrolled_at']


# === 3. Complete Lesson Serializer ===
class CompleteLessonSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()

    def validate_lesson_id(self, value):
        try:
            Lesson.objects.get(id=value)
        except Lesson.DoesNotExist:
            raise serializers.ValidationError("Bunday dars mavjud emas.")
        return value
