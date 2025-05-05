from rest_framework import serializers
from apps.courses.models import Course
from apps.mentors.models import Mentor
from apps.courses.serializers import CourseSerializer
from apps.mentors.serializers import MentorSerializer

class SearchResultSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    mentors = MentorSerializer(many=True)

# apps/search/serializers.py
from rest_framework import serializers
from .models import FilterOptions

class FilterOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterOptions
        fields = ['id', 'name', 'slug']

class FilteredSearchSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    mentors = MentorSerializer(many=True)
    filters = FilterOptionsSerializer(many=True)
    applied_filters = serializers.DictField()