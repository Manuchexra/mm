# mentors/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mentor

User = get_user_model()

@receiver(post_save, sender=User)
def create_mentor_profile(sender, instance, created, **kwargs):
    if created and instance.is_mentor:  # Agar User modelida is_mentor maydoni bo'lsa
        Mentor.objects.create(user=instance)