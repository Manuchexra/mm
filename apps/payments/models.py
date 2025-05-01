from django.db import models
from apps.users.models import User, UserCard
from apps.courses.models import Course

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Yakunlangan'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('refunded', 'Qaytarilgan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    card = models.ForeignKey(UserCard, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_intent_id = models.CharField(max_length=100, blank=True)  # Stripe yoki boshqa platforma uchun

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code