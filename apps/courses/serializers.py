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
# serializers.py
class CourseCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'is_published', 'image']


# === Category ===
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
