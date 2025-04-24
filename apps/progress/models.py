from django.db import models
from apps.users.models import User
from apps.courses.models import Course

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=10)
    
    @property
    def percentage(self):
        if self.total_lessons == 0:
            return 0  # Nolga bo'lishdan himoya qilish
        return int((self.completed_lessons / self.total_lessons) * 100)

    class Meta:
        verbose_name_plural = "Progress"
        unique_together = ['user', 'course']
    