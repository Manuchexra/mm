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

    @swagger_auto_schema(
        operation_description="Obtain access and refresh tokens for user login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Foydalanuvchi nomi yoki email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Parol', format='password'),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    },
                ),
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserRegisterSerializer,
        responses={
            200: openapi.Response(
                description="Successful registration",
                schema=UserRegisterSerializer,
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Confirm user email with a code",
        request_body=ConfirmationCodeSerializer,
        responses={
            200: openapi.Response(
                description="Email confirmed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    },
                ),
            ),
        }
    )
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

    @swagger_auto_schema(
        operation_description="Request password reset by sending a code to email or phone",
        request_body=ResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Code sent successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                ),
            ),
        }
    )
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

    @swagger_auto_schema(
        operation_description="Confirm password reset code",
        request_body=ConfirmationCodeSerializer,
        responses={
            200: openapi.Response(
                description="Code confirmed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    },
                ),
            ),
        }
    )
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

    @swagger_auto_schema(
        operation_description="Set new password after reset",
        request_body=VerifyResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                ),
            ),
        }
    )
    def post(self, request):
        password1 = request.data.get("password_one")
        user = request.user
        user.set_password(password1)
        user.save()

        return Response({"message": "Password changed successfully"}, status=200)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out user by blacklisting refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Logged out successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                ),
            ),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Faqat joriy foydalanuvchi ma'lumotlarini qaytaradi"""
        return self.request.user

    @swagger_auto_schema(
        operation_description="Joriy foydalanuvchi ma'lumotlarini olish",
        responses={
            200: UserAccountSerializer,
        }
    )
    def get(self, request):
        serializer = UserAccountSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Joriy foydalanuvchi ma'lumotlarini yangilash",
        request_body=UserAccountSerializer,
        responses={
            200: UserAccountSerializer,
        }
    )
    def post(self, request):
        serializer = UserAccountSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update user information",
        request_body=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)