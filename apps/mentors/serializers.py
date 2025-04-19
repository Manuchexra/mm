# mentors/serializers.py
from rest_framework import serializers
from .models import Mentor

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id', 'user', 'bio', 'expertise', 'rating', 'is_top_mentor']
        read_only_fields = ['id', 'user']