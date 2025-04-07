from django.contrib import admin

from apps.users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'auth_type', 'auth_status', 'auth_role')


