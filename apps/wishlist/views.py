from rest_framework import viewsets, permissions
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     return Wishlist.objects.none()  # Swagger uchun bo'sh queryset
        return Wishlist.objects.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
