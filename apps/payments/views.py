from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Payment, PromoCode
from .serializers import (
    PaymentSerializer, 
    PaymentCreateSerializer,
    PaymentMethodSerializer,
    PromoCodeSerializer
)
from apps.courses.models import Course
from apps.users.models import UserCard

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PaymentCreateView(APIView):
    """
    Yangi to'lov yaratish uchun endpoint.
    course_id va card_id parametrlarini JSON bodyda qabul qiladi.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['course_id', 'card_id'],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Kurs ID raqami'),
                'card_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Karta ID raqami'),
                'promo_code': openapi.Schema(type=openapi.TYPE_STRING, description='Promo kod (ixtiyoriy)'),
            },
        ),
        responses={
            201: openapi.Response(
                description='To\'lov muvaffaqiyatli yaratildi',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'payment_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'course': openapi.Schema(type=openapi.TYPE_STRING),
                        'card': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )
            ),
            400: 'Noto\'g\'ri so\'rov',
            401: 'Ruxsat etilmagan',
        },
        operation_description="""Yangi to'lov yaratish uchun endpoint. 
        course_id va card_id majburiy parametrlar, promo_code ixtiyoriy."""
    )

    def post(self, request):
        # 1. Ma'lumotlarni validatsiya qilamiz
        serializer = PaymentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Kurs va kartani topamiz
        try:
            course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
            card = get_object_or_404(
                UserCard, 
                id=serializer.validated_data['card_id'],
                user=request.user  # Faqat foydalanuvchining o'z kartasi
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Promo kodni tekshiramiz (agar bor bo'lsa)
        final_amount = course.price
        if 'promo_code' in serializer.validated_data and serializer.validated_data['promo_code']:
            # Bu yerda promo kodni tekshirish logikasi bo'ladi
            pass

        # 4. To'lovni yaratamiz
        try:
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                card=card,
                amount=final_amount,
                status='pending'
            )

            return Response(
                {
                    "status": "success",
                    "payment_id": payment.id,
                    "amount": payment.amount,
                    "course": course.title,
                    "card": f"{card.get_card_type_display()} •••• {card.card_number[-4:]}"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": f"To'lov yaratishda xato: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PromoCodeValidateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'Promo kod kiritilmagan'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            promo = PromoCode.objects.get(
                code=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            return Response(PromoCodeSerializer(promo).data)
        except PromoCode.DoesNotExist:
            return Response(
                {'error': 'Yaroqsiz promo kod'}, 
                status=status.HTTP_400_BAD_REQUEST
            )