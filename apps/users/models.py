from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

import uuid

class UserCustomManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_or_email, password=None, **extra_fields):
        if '@' in phone_or_email:
            email = phone_or_email
            phone = None
            auth_type = 'email'
        else:
            phone = phone_or_email
            email = None
            auth_type = 'phone_number'

        # 🎯 SHU YERDA:
        username = str(uuid.uuid4())  # bu har doim unique bo'ladi

        # majburiy maydonlarni extra_fields orqali to‘ldiramiz
        extra_fields.setdefault("username", username)
        extra_fields.setdefault("auth_type", auth_type)

        user = self.model(
            email=email,
            phone_number=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("username", email)
        extra_fields.setdefault("auth_type", "email")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class OpeningTime(BaseModel):
    class OpeningTimeChoices(models.TextChoices):
        MONDAY = 'Monday'
        TUESDAY = 'Tuesday'
        WEDNESDAY = 'Wednesday'
        THURSDAY = 'Thursday'
        FRIDAY = 'Friday'
        SATURDAY = 'Saturday'
        SUNDAY = 'Sunday'

    day = models.CharField(max_length=10, choices=OpeningTimeChoices.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

class User(AbstractUser):
    class Meta:
        db_table = 'users_user'

    validate_email = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Enter a valid email address'
    )
    validate_phone = RegexValidator(
        regex=r'^\+998\d{9}$',
        message='Enter a valid Uzbekistan phone number starting with +998'
    )

    AUTH_TYPE = (
        ('email', 'Email'),
        ('phone_number', 'Phone number'),
    )
    AUTH_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )
    AUTH_ROLE = (
        ('moderator', 'Moderator'),
        ('seller', 'Seller'),
        ('superuser', 'Superuser'),
        ('buyer', 'Buyer'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)

    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE, default='buyer')
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default='pending')

    image = models.ImageField(upload_to='project/', null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    wallet = models.PositiveIntegerField(default=0, null=True)
    email_confirmed = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    working_hours = models.ManyToManyField(OpeningTime, related_name='working_hours', blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserCustomManager()

    def save(self, *args, **kwargs):
        if self.email_confirmed:
            self.auth_status = 'confirmed'
        else:
            self.auth_status = 'pending'
        super(User, self).save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        # full_name ni avtomatik to'ldirish
        if not self.full_name:
            if self.first_name or self.last_name:
                self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
            elif self.username:
                self.full_name = self.username
        super().save(*args, **kwargs)
    

class UserCard(BaseModel):
    """Foydalanuvchi kredit kartalari"""
    CARD_TYPES = (
        ('uzcard', 'Uzcard'),
        ('humo', 'Humo'),
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('unionpay', 'UnionPay'),
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='cards'
    )
    card_type = models.CharField(
        max_length=20, 
        choices=CARD_TYPES,
        verbose_name="Karta turi"
    )
    card_number = models.CharField(
        max_length=16,
        verbose_name="Karta raqami"
    )
    expire_date = models.CharField(
        max_length=5,  # MM/YY formatida
        verbose_name="Amal qilish muddati"
    )
    card_holder = models.CharField(
        max_length=100,
        verbose_name="Karta egasi"
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="Asosiy karta"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )

    class Meta:
        db_table = 'users_card'
        verbose_name = "Foydalanuvchi kartasi"
        verbose_name_plural = "Foydalanuvchi kartalari"
        ordering = ['-is_default', '-created_at']
        unique_together = ['user', 'card_number']

    def __str__(self):
        return f"{self.get_card_type_display()} •••• {self.card_number[-4:]}"

    def save(self, *args, **kwargs):
        """Asosiy karta sifatida saqlashda boshqa kartalarni is_default=False qilish"""
        if self.is_default:
            UserCard.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def mask_card_number(self):
        """Karta raqamini yashirish"""
        return f"•••• •••• •••• {self.card_number[-4:]}"
    def save(self, *args, **kwargs):
        # full_name ni avtomatik to'ldirish
        if not self.full_name and self.username:
            self.full_name = self.username
        super().save(*args, **kwargs)