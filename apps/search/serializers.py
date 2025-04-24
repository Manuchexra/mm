from rest_framework import serializers
from apps.courses.models import Course
from apps.mentors.models import Mentor
from apps.courses.serializers import CourseSerializer
from apps.mentors.serializers import MentorSerializer

class SearchResultSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    mentors = MentorSerializer(many=True)
