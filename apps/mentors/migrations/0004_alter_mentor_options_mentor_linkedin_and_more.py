# Generated by Django 5.2 on 2025-04-24 15:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0003_alter_mentor_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mentor',
            options={'ordering': ['-rating', 'user__email'], 'verbose_name': 'Mentor', 'verbose_name_plural': 'Mentors'},
        ),
        migrations.AddField(
            model_name='mentor',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn profile'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='secondary_expertise',
            field=models.CharField(blank=True, choices=[('WD', 'Web Development'), ('DS', 'Data Science'), ('DE', 'Design'), ('BU', 'Business'), ('MA', 'Marketing'), ('LA', 'Language')], max_length=2, null=True, verbose_name='Secondary expertise'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Personal website'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='years_experience',
            field=models.PositiveIntegerField(default=1, verbose_name='Years of experience'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='mentors/avatars/%Y/%m/%d/', verbose_name='Profile picture'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='bio',
            field=models.TextField(blank=True, help_text='Tell us about your professional background', verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expertise',
            field=models.CharField(choices=[('WD', 'Web Development'), ('DS', 'Data Science'), ('DE', 'Design'), ('BU', 'Business'), ('MA', 'Marketing'), ('LA', 'Language')], default='WD', max_length=2, verbose_name='Primary expertise area'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='is_top_mentor',
            field=models.BooleanField(default=False, verbose_name='Top mentor status'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Average rating'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last updated'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL, verbose_name='User account'),
        ),
        migrations.AddIndex(
            model_name='mentor',
            index=models.Index(fields=['is_top_mentor'], name='mentors_men_is_top__7ff817_idx'),
        ),
        migrations.AddIndex(
            model_name='mentor',
            index=models.Index(fields=['expertise'], name='mentors_men_experti_e1c773_idx'),
        ),
    ]
