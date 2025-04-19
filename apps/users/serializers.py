import re
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from .utils import (
    send_confirmation_code_to_user,
    generate_confirmation_code,
    send_verification_code_to_user,
)


def is_phone(phone):
    return bool(re.match(r"^\+998\d{9}$", phone))


def is_email(email):
    # ✅ To'g'rilangan regex: "\\" emas, balki "\" bo'lishi kerak edi
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


class UserRegisterSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_or_email = attrs.get("phone_or_email")

        if is_phone(phone_or_email):
            attrs["auth_type"] = "phone_number"
        elif is_email(phone_or_email):
            attrs["auth_type"] = "email"
        else:
            raise ValidationError({"phone_or_email": "Email yoki telefon raqam noto'g'ri"})

        return attrs

    def create(self, validated_data):
        phone_or_email = validated_data["phone_or_email"]
        password = validated_data["password"]
        auth_type = validated_data["auth_type"]

        if auth_type == "phone_number":
            user, created = User.objects.get_or_create(phone_number=phone_or_email)
        else:
            user, created = User.objects.get_or_create(email=phone_or_email)

        if not created and user.auth_status == "confirmed":
            raise ValidationError({"phone_or_email": "Bu foydalanuvchi allaqachon ro'yxatdan o'tgan"})

        user.username = phone_or_email
        user.auth_type = auth_type
        user.auth_role = "buyer"
        user.set_password(password)
        user.save()

        confirmation_code = generate_confirmation_code()
        cache.set(f"confirmation_code_{user.id}", confirmation_code, timeout=300)

        if auth_type == "email":
            send_confirmation_code_to_user(user, confirmation_code)
        else:
            send_verification_code_to_user(user.phone_number, confirmation_code)

        return user

    def to_representation(self, instance):
        return {"user_id": instance.id, "auth_type": instance.auth_type}


class ConfirmationCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.IntegerField()


class ResetPasswordSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()


class VerifyResetPasswordSerializer(serializers.Serializer):
    password_one = serializers.CharField()


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name", "phone_number", "image", "bio",
            "country", "specialization", "wallet"
        ]
