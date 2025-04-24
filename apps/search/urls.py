from django.urls import path
from .views import search

app_name = 'search'

urlpatterns = [
    path('search/', search, name='search-api'),
    
]