from django.contrib import admin
from .models import Category, Course, Section, Lesson

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'description', 'instructor__username')
    inlines = [SectionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section__course',)
    search_fields = ('title', 'content')
