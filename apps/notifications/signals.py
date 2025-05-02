from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment
from .models import Notification

@receiver(post_save, sender=Payment)
def create_payment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="To'lov muvaffaqiyatli amalga oshirildi",
            message=f"Siz {instance.course.title} kursi uchun to'lov amalga oshirdingiz",
            notification_type='payment'
        )