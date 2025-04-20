# serializers.py faylida
from rest_framework import serializers
from .models import Mentor

class MentorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Mentor
        fields = [
            'id', 'user', 'full_name', 'email', 
            'avatar', 'avatar_url', 'bio', 'expertise',
            'rating', 'is_top_mentor', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'rating', 'created_at']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        return None