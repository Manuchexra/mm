from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'course', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating 1 dan 5 gacha bo‘lishi kerak.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return Review.objects.create(user=user, **validated_data)
