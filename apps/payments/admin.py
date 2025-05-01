from django.contrib import admin
from .models import Payment, PromoCode
from django.utils.html import format_html
from django.db.models import Sum

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_info', 
        'course_info', 
        'amount', 
        'status', 
        'payment_date', 
        'card_info'
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = (
        'user__username', 
        'user__email', 
        'user__phone_number',
        'course__title',
        'payment_intent_id'
    )
    readonly_fields = ('created_at', 'updated_at', 'payment_intent_id')
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions = ['mark_as_completed', 'mark_as_refunded']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('user', 'course', 'card', 'amount', 'status')
        }),
        ('To\'lov tafsilotlari', {
            'fields': ('payment_intent_id', 'created_at', 'updated_at')
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

    def course_info(self, obj):
        if obj.course:
            return format_html(
                '<a href="/admin/courses/course/{}/change/">{}</a>',
                obj.course.id,
                obj.course.title
            )
        return "-"
    course_info.short_description = "Kurs"

    def card_info(self, obj):
        if obj.card:
            return f"{obj.card.get_card_type_display()} •••• {obj.card.card_number[-4:]}"
        return "-"
    card_info.short_description = "Karta"

    def payment_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    payment_date.short_description = "To'lov vaqti"
    payment_date.admin_order_field = 'created_at'

    def mark_as_completed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='completed')
        self.message_user(request, f"{updated} ta to'lov yakunlandi deb belgilandi")
    mark_as_completed.short_description = "Tanlangan to'lovlarni yakunlangan deb belgilash"

    def mark_as_refunded(self, request, queryset):
        updated = queryset.filter(status='completed').update(status='refunded')
        self.message_user(request, f"{updated} ta to'lov qaytarilgan deb belgilandi")
    mark_as_refunded.short_description = "Tanlangan to'lovlarni qaytarilgan deb belgilash"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'course', 'card')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 
        'discount_percent', 
        'validity_period', 
        'is_active', 
        'used_count',
        'total_discount'
    )
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    readonly_fields = ('used_count', 'total_discount')
    list_editable = ('is_active',)

    fieldsets = (
        (None, {
            'fields': ('code', 'discount_percent', 'is_active')
        }),
        ('Amal qilish muddati', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Statistika', {
            'fields': ('used_count', 'total_discount'),
            'classes': ('collapse',)
        }),
    )

    def validity_period(self, obj):
        return f"{obj.valid_from.strftime('%d.%m.%Y')} - {obj.valid_to.strftime('%d.%m.%Y')}"
    validity_period.short_description = "Amal qilish muddati"

    def used_count(self, obj):
        return Payment.objects.filter(promo_code=obj).count()
    used_count.short_description = "Foydalanishlar soni"

    def total_discount(self, obj):
        result = Payment.objects.filter(
            promo_code=obj
        ).aggregate(total=Sum('amount'))['total']
        return f"${result or 0}"
    total_discount.short_description = "Jami chegirma"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _used_count=Count('payment'),
            _total_discount=Sum('payment__amount')
        )