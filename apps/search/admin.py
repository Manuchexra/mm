# search/admin.py
from django.contrib import admin
from .models import SearchHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')  # 'created_at' emas
    list_filter = ('timestamp',)  # 'created_at' emas
