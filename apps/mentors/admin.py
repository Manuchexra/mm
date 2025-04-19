# mentors/admin.py
from django.contrib import admin
from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'rating', 'is_top_mentor')
    list_filter = ('is_top_mentor', 'expertise')
    search_fields = ('user__username', 'user__email', 'expertise')