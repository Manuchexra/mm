from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# search/models.py
class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  # Bu bor edi

    def __str__(self):
        return f"{self.user.username} searched: {self.query}"


# apps/search/models.py
class FilterOptions(models.Model):
    name = models.CharField(max_length=100)  # Kategoriya nomi
    slug = models.SlugField(unique=True)     # URL uchun
    
    def __str__(self):
        return self.name