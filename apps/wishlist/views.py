from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistCreateSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Wishlist.objects.none()
        return Wishlist.objects.filter(user=self.request.user).select_related('course', 'user')

    def get_serializer_class(self):
        if self.action == 'create':
            return WishlistCreateSerializer
        return WishlistSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Course ID to add to wishlist'
                )
            },
            required=['course_id']
        ),
        responses={
            201: WishlistSerializer,
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if Wishlist.objects.filter(
            user=request.user,
            course=serializer.validated_data['course']
        ).exists():
            return Response(
                {"detail": "This course is already in your wishlist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist = Wishlist.objects.create(
            user=request.user,
            course=serializer.validated_data['course']
        )
        
        return Response(
            WishlistSerializer(wishlist, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        responses={200: WishlistSerializer(many=True)}
    )
    @action(detail=False, methods=['GET'])
    def mine(self, request):
        """Get current user's wishlist"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)