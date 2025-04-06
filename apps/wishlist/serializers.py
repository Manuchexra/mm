from rest_framework import serializers
from .models import Wishlist  # 🟢 To‘g‘ri

class WishlistSerializer(serializers.ModelSerializer):  # ✅ SHU BO‘LISHI KERAK
    user = serializers.StringRelatedField(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.ImageField(source='course.image', read_only=True)
    instructor = serializers.CharField(source='course.instructor.username', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'course', 'course_title', 'course_image', 'instructor', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Wishlist.objects.create(user=user, **validated_data)
