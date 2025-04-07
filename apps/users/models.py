from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserCustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


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
    _validate_email = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Enter a valid email address'
    )
    _validate_phone_number = RegexValidator(
        regex=r"^9\d{12}$",
        message='Enter a valid phone number'
    )

    AUTH_TYPE = (
        ('email', 'email'),
        ('phone_number', 'phone_number'),
    )
    AUTH_STATUS = (
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
    )

    AUTH_ROLE = (
        ('moderator', 'moderator'),
        ('seller', 'seller'),
        ('superuser', 'superuser'),
        ('buyer', 'buyer'),
    )

    first_name = None
    last_name = None
    full_name = models.CharField(max_length=255, blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE, default='buyer')
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    image = models.ImageField(upload_to='project/', null=True)
    email = models.EmailField(blank=True, validators=[_validate_email])
    wallet = models.PositiveIntegerField(null=True, default=0)
    email_confirmed = models.BooleanField(default=False)
    working_hours = models.ManyToManyField(OpeningTime, related_name='working_hours')
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default='pending')
    country = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)

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