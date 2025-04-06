from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at', 'course')
    search_fields = ('user__username', 'course__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
