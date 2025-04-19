from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    is_top_mentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Mentor)"