# apps/search/urls.py
from django.urls import path
from .views import search, search_with_filters

urlpatterns = [
    path('', search, name='search'),
    path('filter/', search_with_filters, name='search-filter'),
]