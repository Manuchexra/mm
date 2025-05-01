from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from rest_framework import serializers
import re
from rest_framework import generics
from . import models
from .models import User
from .utils import send_confirmation_code_to_user, generate_confirmation_code, send_verification_code_to_user


def is_phone(phone):
    phone_regex = r"^\+998\d{9}$"
    return bool(re.match(phone_regex, phone))


def is_email(email):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))


class UserSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_or_email = attrs.get('phone_or_email')
        if is_phone(phone_or_email):
            auth_type = 'phone_number'
        elif is_email(phone_or_email):
            auth_type = 'email'
        else:
            raise serializers.ValidationError(
                detail={'phone_or_email': "Iltimos, telefon raqam yoki email kiritishingiz kerak."}
            )
        attrs['auth_type'] = auth_type
        return super().validate(attrs)

    def create(self, validated_data):
        phone_or_email = validated_data.get('phone_or_email')
        password = validated_data.get('password')
        auth_type = validated_data.get('auth_type')

        username = phone_or_email
        if auth_type == 'phone_number':
            user, created = User.objects.get_or_create(phone_number=phone_or_email)
        else:
            user, created = User.objects.get_or_create(email=phone_or_email)

            if not created and user.auth_status == 'confirmed':
                raise ValidationError(detail={'phone_or_email': "Bunday foydalanuvchi allaqachon mavjud"})

        user.username = username
        user.auth_type = auth_type
        user.auth_role = "seller"
        user.set_password(password)
        user.save()
        confirmation_code = generate_confirmation_code()
        cache.set(f"confirmation_code_{user.id}", confirmation_code, timeout=300)
        print(confirmation_code)
        print(cache.get(f"confirmation_code_{user.id}"))
        if auth_type == 'email':
            send_confirmation_code_to_user(user, confirmation_code)
        elif auth_type == 'phone_number':
            send_verification_code_to_user(user.phone_number, confirmation_code)

        return user

    def to_representation(self, instance):
        return {
            'user_id': instance.id
        }


class ConfirmationCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.IntegerField()


class ResetPasswordSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()


class VerifyResetPassword(serializers.Serializer):
    password_one = serializers.CharField()

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'country', 'gender']
        read_only_fields = ['id']  # username o‘zgartirilsa, bu yerdan ham olib tashlanadi

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.country = validated_data.get('country', instance.country)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


from rest_framework import serializers
from .models import UserCard

class UserCardSerializer(serializers.ModelSerializer):
    masked_number = serializers.SerializerMethodField()
    card_type_display = serializers.SerializerMethodField()

    class Meta:
        model = UserCard
        fields = [
            'id',
            'card_type',
            'card_type_display',
            'card_number',
            'masked_number',
            'expire_date',
            'card_holder',
            'is_default',
            'is_active',
            'created_at'
        ]
        extra_kwargs = {
            'card_number': {'write_only': True}
        }

    def get_masked_number(self, obj):
        return obj.mask_card_number()

    def get_card_type_display(self, obj):
        return obj.get_card_type_display()

    def validate_card_number(self, value):
        """Karta raqamini tekshirish"""
        if not value.isdigit() or len(value) not in (16, 19):
            raise serializers.ValidationError("Noto'g'ri karta raqami formati")
        return value

    def validate_expire_date(self, value):
        """Amal qilish muddatini tekshirish"""
        if len(value) != 5 or value[2] != '/':
            raise serializers.ValidationError("Noto'g'ri format. MM/YY ko'rinishida bo'lishi kerak")
        return value

