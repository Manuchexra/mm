from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Jadvalda ko‘rinadigan ustunlar
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_instructor', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_instructor', 'is_active')
    
    # Tartiblash (search) imkoniyatlari
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Maydonlarni qanday guruhlarga ajratamiz (edit page uchun)
    fieldsets = (
        (_('Login Maʼlumotlari'), {'fields': ('username', 'password')}),
        (_('Shaxsiy Maʼlumotlar'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Ruxsatlar'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Muallimmi?'), {'fields': ('is_instructor',)}),
        (_('Muhim sanalar'), {'fields': ('last_login', 'date_joined')}),
    )

    # Yangi foydalanuvchi yaratishda ko‘rinadigan maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_instructor', 'is_active', 'is_staff'),
        }),
    )
