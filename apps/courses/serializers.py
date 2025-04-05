from rest_framework import serializers
from .models import Category, Course, Section, Lesson


# === Lesson ===
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'content', 'order']


# === Section ===
class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'order', 'lessons']


# === Course List/Detail ===
class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'category',
            'price',
            'image',
            'is_published',
            'created_at',
            'instructor',
            'sections',
        ]


# === Course Creation ===
class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'category',
            'price',
            'image',
            'is_published'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Course.objects.create(instructor=user, **validated_data)


# === Category ===
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
