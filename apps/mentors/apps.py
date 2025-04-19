# mentors/apps.py
from django.apps import AppConfig

class MentorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mentors'

    def ready(self):
        import apps.mentors.signals