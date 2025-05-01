from django.urls import path
from .views import (
    PaymentListView,
    PaymentCreateView,
    PromoCodeValidateView
)

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('promo/validate/', PromoCodeValidateView.as_view(), name='promo-validate'),
]