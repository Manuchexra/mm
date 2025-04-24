from django.urls import path
from .views import ProgressAPIView

urlpatterns = [
    path('progress/<int:course_id>/', ProgressAPIView.as_view(), name='progress'),
]