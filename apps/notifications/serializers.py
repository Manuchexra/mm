from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 'created_at', 'time_since']
    
    def get_time_since(self, obj):
        from django.utils.timesince import timesince
        return timesince(obj.created_at)