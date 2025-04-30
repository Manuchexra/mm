# serializers.py
from rest_framework import serializers
from .models import Wishlist
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer

class WishlistSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.id')
    course_title = serializers.CharField(source='course.title')
    course_image = serializers.ImageField(source='course.image')
    category_name = serializers.CharField(source='course.category.name')
    price = serializers.DecimalField(source='course.price', max_digits=10, decimal_places=2)
    instructor = serializers.CharField(source='course.instructor.username', read_only=True)
    # user_id = serializers.IntegerField(source='user.id', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Wishlist
        fields = [
            'id',
            # 'user_id',
            'course_id',
            'course_title',
            'course_image',
            'category_name',  # Yangi qo'shildi
            'price',          # Yangi qo'shildi
            'instructor',
            'created_at'
        ]
        read_only_fields = fields



class WishlistCreateSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        source='course'
    )
