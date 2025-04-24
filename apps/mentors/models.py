from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Mentor(models.Model):
    class ExpertiseArea(models.TextChoices):
        WEB_DEV = 'WD', _('Web Development')
        DATA_SCIENCE = 'DS', _('Data Science')
        DESIGN = 'DE', _('Design')
        BUSINESS = 'BU', _('Business')
        MARKETING = 'MA', _('Marketing')
        LANGUAGE = 'LA', _('Language')

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mentor_profile',
        verbose_name=_('User account')
    )
    avatar = models.ImageField(
        upload_to='mentors/avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('Profile picture')
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_('Biography'),
        help_text=_('Tell us about your professional background')
    )
    expertise = models.CharField(
        max_length=2,
        choices=ExpertiseArea.choices,
        default=ExpertiseArea.WEB_DEV,
        verbose_name=_('Primary expertise area')
    )
    secondary_expertise = models.CharField(
        max_length=2,
        choices=ExpertiseArea.choices,
        blank=True,
        null=True,
        verbose_name=_('Secondary expertise')
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name=_('Average rating')
    )
    is_top_mentor = models.BooleanField(
        default=False,
        verbose_name=_('Top mentor status')
    )
    years_experience = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Years of experience')
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Personal website')
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('LinkedIn profile')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last updated')
    )

    class Meta:
        verbose_name = _('Mentor')
        verbose_name_plural = _('Mentors')
        ordering = ['-rating', 'user__email']  # Using email which definitely exists
        indexes = [
            models.Index(fields=['is_top_mentor']),
            models.Index(fields=['expertise']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_expertise_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    def update_rating(self, new_rating):
        """Update mentor's average rating"""
        self.rating = (self.rating + new_rating) / 2
        self.save()
        return self.rating