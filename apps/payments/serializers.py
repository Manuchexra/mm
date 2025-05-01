from rest_framework import serializers
from .models import Payment, PromoCode
from apps.courses.serializers import CourseSerializer
from apps.users.serializers import UserCardSerializer

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'discount_percent', 'valid_from', 'valid_to']

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    card = UserCardSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'course', 'card', 'amount', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.Serializer):
    """
    To'lov yaratish uchun serializer. 
    course_id va card_id majburiy, promo_code ixtiyoriy.
    """
    course_id = serializers.IntegerField(
        required=True,
        help_text="Kursning ID raqami",
        error_messages={
            'required': 'Kurs IDsi kiritilishi shart',
            'invalid': 'Kurs IDsi raqam bo\'lishi kerak'
        }
    )
    
    card_id = serializers.IntegerField(
        required=True,
        help_text="Kartaning ID raqami",
        error_messages={
            'required': 'Karta IDsi kiritilishi shart',
            'invalid': 'Karta IDsi raqam bo\'lishi kerak'
        }
    )
    
    promo_code = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Promo kod (ixtiyoriy)"
    )

    def validate_course_id(self, value):
        """Kurs mavjudligini tekshiramiz"""
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday IDga ega kurs topilmadi")
        return value

    def validate_card_id(self, value):
        """Karta mavjudligini tekshiramiz"""
        if not UserCard.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday IDga ega karta topilmadi")
        return value

class PaymentMethodSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    expiry_date = serializers.CharField(max_length=5)
    cvc = serializers.CharField(max_length=4)