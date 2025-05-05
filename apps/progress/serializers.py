# serializers.py
from rest_framework import serializers
from .models import Progress

class ProgressSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()  # Yangi field qo'shamiz
    
    class Meta:
        model = Progress
        fields = ['id', 'completed_lessons', 'total_lessons', 'user', 'course', 'percentage']  # percentage ni qo'shamiz
    
    def get_percentage(self, obj):
        return obj.percentage  