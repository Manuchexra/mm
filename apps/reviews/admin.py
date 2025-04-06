from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('course', 'rating', 'created_at')
    search_fields = ('user__username', 'course__title', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
