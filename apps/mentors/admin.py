# admin.py faylida
from django.contrib import admin
from django.utils.html import format_html
from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'expertise', 'rating', 'is_top_mentor')
    list_filter = ('expertise', 'is_top_mentor')
    search_fields = ('user__first_name', 'user__last_name', 'bio')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "No Avatar"
    avatar_preview.short_description = 'Avatar'