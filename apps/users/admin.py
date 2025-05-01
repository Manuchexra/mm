from django.contrib import admin

from apps.users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'auth_type', 'auth_status', 'auth_role')


from django.contrib import admin
from .models import User, UserCard, OpeningTime
from django.utils.html import format_html

@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'card_type_display', 'masked_number', 'expire_date', 'is_default', 'is_active')
    list_filter = ('card_type', 'is_default', 'is_active')
    search_fields = ('user__username', 'user__email', 'card_number', 'card_holder')
    list_editable = ('is_default', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'masked_number_display')
    fieldsets = (
        (None, {
            'fields': ('user', 'card_type')
        }),
        ('Karta Ma\'lumotlari', {
            'fields': ('card_number', 'expire_date', 'card_holder')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active')
        }),
        ('Qo\'shimcha', {
            'fields': ('created_at', 'updated_at', 'masked_number_display'),
            'classes': ('collapse',)
        }),
    )

    def user_info(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/users/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.get_full_name() or obj.user.username
            )
        return "-"
    user_info.short_description = "Foydalanuvchi"
    user_info.admin_order_field = 'user__username'

    def card_type_display(self, obj):
        return obj.get_card_type_display()
    card_type_display.short_description = "Karta Turi"

    def masked_number(self, obj):
        return obj.mask_card_number()
    masked_number.short_description = "Karta Raqami"

    def masked_number_display(self, obj):
        return obj.mask_card_number()
    masked_number_display.short_description = "Karta Raqami (Yashirilgan)"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')