# mentors/urls.py
from django.urls import path
from .views import MentorListView, MentorDetailView, TopMentorListView

urlpatterns = [
    path('', MentorListView.as_view(), name='mentor-list'),
    path('<int:pk>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('top/', TopMentorListView.as_view(), name='top-mentor-list'),
]