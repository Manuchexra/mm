from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache

from .models import User
from .serializers import (
    UserSerializer,
    ConfirmationCodeSerializer,
    ResetPasswordSerializer,
    VerifyResetPassword,
    UserAccountSerializer,
    UserUpdateSerializer,
    is_email,
    is_phone
)
from .utils import send_confirmation_code_to_user, generate_confirmation_code, send_verification_code_to_user
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=TokenObtainPairSerializer,
        responses={
            200: openapi.Response(
                description="Successful login with access and refresh tokens",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    },
                    required=['refresh', 'access']
                )
            ),
            400: "Invalid credentials",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserRegisterAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="User successfully registered",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the registered user')
                    },
                    required=['user_id']
                )
            ),
            400: "Invalid input data"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=200)
        return Response(serializer.errors, status=400)

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all users",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                            'auth_status': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication status'),
                        }
                    )
                )
            ),
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ConfirmationCodeSerializer,
        responses={
            200: openapi.Response(
                description="Email confirmed successfully with tokens",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    },
                    required=['refresh', 'access']
                )
            ),
            400: "Invalid or expired code",
            404: "User not found"
        }
    )
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user_id = serializer.validated_data["user_id"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        cached_code = cache.get(f"confirmation_code_{user.id}")
        if not cached_code:
            return Response({"error": "Invalid or expired code"}, status=400)

        # Convert cached_code to integer for comparison
        try:
            cached_code = int(cached_code)
        except (ValueError, TypeError):
            return Response({"error": "Invalid or expired code"}, status=400)

        if cached_code != code:
            return Response({"error": "Invalid or expired code"}, status=400)

        user.auth_status = 'confirmed'
        user.save()
        return Response(user.tokens(), status=200)
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Confirmation code sent to user",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmation message'),
                    },
                    required=['user_id', 'message']
                )
            ),
            400: "Invalid email or phone",
            404: "User not found"
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
        request_body=ConfirmationCodeSerializer,
        responses={
            200: openapi.Response(
                description="Reset code confirmed successfully with tokens",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    },
                    required=['refresh', 'access']
                )
            ),
            400: "Invalid or expired code",
            404: "User not found"
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
        request_body=VerifyResetPassword,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                    required=['message']
                )
            ),
            400: "Invalid input data",
            401: "Unauthorized"
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token')
            }
        ),
        responses={
            205: openapi.Response(
                description="Logged out successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                    required=['message']
                )
            ),
            400: "Invalid refresh token",
            401: "Unauthorized"
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

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Foydalanuvchi ma'lumotlari muvaffaqiyatli olindi",
                schema=UserAccountSerializer
            ),
            401: "Ruxsatsiz kirish"
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
            400: "Noto‘g‘ri ma'lumotlar kiritildi",
            401: "Ruxsatsiz kirish"
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
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(
                description="User details updated successfully",
                schema=UserUpdateSerializer
            ),
            400: "Invalid input data",
            401: "Unauthorized",
            404: "User not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)