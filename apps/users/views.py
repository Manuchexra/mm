from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserRegisterSerializer,
    ConfirmationCodeSerializer,
    ResetPasswordSerializer,
    VerifyResetPasswordSerializer,
    UserAccountSerializer,
    UserUpdateSerializer,
    is_email,
    is_phone
)
from .utils import send_confirmation_code_to_user, generate_confirmation_code, send_verification_code_to_user

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/swagger/')


class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ConfirmationCodeSerializer)
    def post(self, request):
        user_id = request.data.get("user_id")
        code = request.data.get("code")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        cached_code = cache.get(f"confirmation_code_{user.id}")
        if not cached_code or str(cached_code) != str(code):
            return Response({"error": "Invalid or expired code"}, status=400)

        user.auth_status = 'confirmed'
        user.save()
        return Response(user.tokens(), status=200)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        phone_or_email = request.data.get('phone_or_email')

        if is_email(phone_or_email):
            user = User.objects.filter(email=phone_or_email).first()
        elif is_phone(phone_or_email):
            user = User.objects.filter(phone_number=phone_or_email).first()
        else:
            return Response({"error": "Invalid email or phone"}, status=400)

        if not user:
            return Response({"error": "User not found"}, status=404)

        code = generate_confirmation_code()
        cache.set(f"confirmation_code_{user.id}", code, timeout=300)

        if is_email(phone_or_email):
            send_confirmation_code_to_user(user, code)
        else:
            send_verification_code_to_user(user.phone_number, code)

        return Response({"user_id": user.id, "message": "Code sent"}, status=200)


class ConfirmResetCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ConfirmationCodeSerializer)
    def post(self, request):
        user_id = request.data.get("user_id")
        code = request.data.get("code")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        cached_code = cache.get(f"confirmation_code_{user.id}")
        if not cached_code or str(cached_code) != str(code):
            return Response({"error": "Invalid or expired code"}, status=400)

        return Response(user.tokens(), status=200)


class ConfirmPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=VerifyResetPasswordSerializer)
    def post(self, request):
        password1 = request.data.get("password_one")
        password2 = request.data.get("password_two")

        if password1 != password2:
            return Response({"error": "Passwords do not match"}, status=400)

        user = request.user
        user.set_password(password1)
        user.save()

        return Response({"message": "Password changed successfully"}, status=200)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



class UserAccountAPIView(generics.RetrieveAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Faqat joriy foydalanuvchi ma'lumotlarini qaytaradi"""
        return self.request.user



class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

