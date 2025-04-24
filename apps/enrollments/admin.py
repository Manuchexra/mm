from django.contrib import admin
from .models import Enrollment, LessonProgress, Progress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    ordering = ('-enrolled_at',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'lesson__section__course')
    search_fields = ('enrollment__user__username', 'lesson__title')
    ordering = ('-completed_at',)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'percentage')
    list_filter = ('course',)
