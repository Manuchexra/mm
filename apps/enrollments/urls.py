from django.urls import path
from .views import (
    EnrollView,
    MyEnrollmentsView,
    MyCourseProgressView,
    CompleteLessonView
)

urlpatterns = [
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('my/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('progress/<int:course_id>/', MyCourseProgressView.as_view(), name='course-progress'),
    path('complete/<int:course_id>/', CompleteLessonView.as_view(), name='complete-lesson'),
]
