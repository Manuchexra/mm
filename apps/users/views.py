from rest_framework import generics
from .serializers import UserSerializer, ConfirmationCodeSerializer, ResetPasswordSerializer, VerifyResetPassword
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers, models
from .models import User
from .serializers import is_email, is_phone
from .utils import send_confirmation_code_to_user, generate_confirmation_code, send_verification_code_to_user


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConfirmEmailView(APIView):
    @swagger_auto_schema(request_body=ConfirmationCodeSerializer)
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        if user_id is None:
            return Response(
                data={"error": "user_id junatilmadi!"}, status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = request.data.get('code')
        try:
            user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            return Response(
                {"error": "Bunday foydalanuvchi mavjud emas!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cached_code = cache.get(f"confirmation_code_{user.id}")
        print(cached_code)

        if not cached_code:
            return Response(
                data={
                    "error": "Tasdiqlash kodi muddati o'tgan yoki mavjud emas."
                    }, status=status.HTTP_400_BAD_REQUEST)

        if cached_code != confirmation_code:
            return Response(
                data={"error": "Tasdiqlash kodi noto'g'ri!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.auth_status = 'confirmed'
        user.save()
        return Response(data=user.tokens(), status=status.HTTP_201_CREATED)


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request, *args, **kwargs):
        phone_or_email = self.request.data.get('phone_or_email', None)
        if phone_or_email is None:
            return Response(
                {"error": "Telefon raqam yoki elektron pochta manzilni qo'shing"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if is_email(phone_or_email):
            user = User.objects.filter(email=phone_or_email).first()
            if user is None:
                return Response(
                    {"error": "Bunday foydalanuvchi mavjud emas!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            code = generate_confirmation_code()
            send_confirmation_code_to_user(user, code)
            cache.set(f"confirmation_code_{user.id}", code, timeout=300)
        elif is_phone(phone_or_email):
            user = User.objects.filter(phone_number=phone_or_email).first()
            if user is None:
                return Response(
                    {"error": "Bunday foydalanuvchi mavjud emas!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            code = generate_confirmation_code()
            send_verification_code_to_user(user.phone_number, code)
            cache.set(f"confirmation_code_{user.id}", code, timeout=300)
        
        else:
            return Response(
                data={"error": "email yoki telifon nomer kiriting!"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data= {
                "user_id": user.id,
                "code": "Kode muvoffaqiyatli junatildi"
            }, 
            status=status.HTTP_200_OK
        )

class ConfirmCodeView(APIView):
    @swagger_auto_schema(request_body=ConfirmationCodeSerializer)
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id", None)
        code = request.data.get("code", None)

        if user_id is None:
            return Response(
                data={
                   "error": "user_id topilmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if code is None:
            return Response(
                data={
                   "error": "kode kelmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        confirmation_code = request.data.get('code')
        try:
            user = User.objects.get(id=int(user_id), auth_status='confirmed')
        except (User.DoesNotExist, ValueError):
            return Response(
                {"error": "Bunday foydalanuvchi mavjud emas!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cached_code = cache.get(f"confirmation_code_{user.id}")

        if not cached_code:
            return Response(
                data={
                    "error": "Tasdiqlash kodi muddati o'tgan yoki mavjud emas."
                    }, status=status.HTTP_400_BAD_REQUEST)

        if cached_code != confirmation_code:
            return Response(
                data={"error": "Tasdiqlash kodi noto'g'ri!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        return Response(data=user.tokens(), status=status.HTTP_201_CREATED)
        
    
class ConfirmPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=VerifyResetPassword)
    def post(self, request, *args, **kwargs):
        user = request.user
        user_password_one = request.data.get("password_one", None)
        user_password_two = request.data.get("password_two", None)
       
        if user is None:
            return Response(
                data={
                   "error": "user topilmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_password_one is None:
            return Response(
                data={
                   "error": "Parol junatilmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_password_two is None:
            return Response(
                data={
                   "error": "Parol junatilmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if user_password_one != user_password_two:
            return Response(
                data={
                    "error": "Parollar mos kelmadi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(user_password_one)
        user.save()
        return Response(
            data={
                "password": "parolingiz yangilandi!"
            }, status=status.HTTP_200_OK
        )   


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class UserAccountAPIView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserAccountSerializer


