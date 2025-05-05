from rest_framework import serializers
from .models import Category, Course, Section, Lesson
from apps.wishlist.models import Wishlist
from apps.mentors.serializers import MentorSerializer


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
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_wishlist = serializers.SerializerMethodField()  # Moved outside Meta
    
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'category',          # kategoriya IDsi
            'category_name',     # kategoriya nomi
            'price',
            'image',
            'is_published',
            'created_at',
            'instructor',
            'sections',
            'is_in_wishlist'     # Wishlist statusi
        ]
    
    def get_is_in_wishlist(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, course=obj).exists()
        return False


# === Course Creation ===
# serializers.py
class CourseCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    image = serializers.ImageField(required=False)
    instructor = MentorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'is_published', 'image','instructor']

        def validate_instructor(self, value):
            # Agar instructor ko'rsatilmagan bo'lsa, joriy foydalanuvchi mentor bo'lsa, uni instructor qilib belgilaymiz
            if not value and hasattr(self.context['request'].user, 'mentor_profile'):
                return self.context['request'].user.mentor_profile
            return value


# === Category ===
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
