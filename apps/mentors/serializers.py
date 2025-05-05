# apps/mentors/serializers.py
from rest_framework import serializers
from .models import Mentor
from apps.users.models import User

class MentorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

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
            request = self.context.get('request')
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None
    def get_full_name(self, obj):
        user = obj.user
        if user.full_name:
            return user.full_name
        # 2. Agar username mavjud bo'lsa
        elif user.username and user.username != user.email:
            return user.username
        
        # 3. Emaildan foydalanamiz
        elif user.email:
            return user.email.split('@')[0]
        
        # 4. Oxirgi chora
        return f"User-{user.id}"

    def get_email(self, obj):
        return obj.user.email