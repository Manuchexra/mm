# admin.py faylida
from django.contrib import admin
from django.utils.html import format_html
from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_preview', 'expertise', 'is_top_mentor')
    list_filter = ('is_top_mentor', 'expertise')
    search_fields = ('user__username', 'user__email', 'expertise')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "No Avatar"
    avatar_preview.short_description = 'Avatar'