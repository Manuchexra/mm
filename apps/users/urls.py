from django.urls import path
from .views import (
    UserRegisterAPIView,
    ConfirmEmailView,
    ResetPasswordView,
    ConfirmResetCodeView,
    ConfirmPasswordView,
    LogoutView,
    UserAccountAPIView,
    UserUpdateAPIView,
    LoginAPIView
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/confirm-code/', ConfirmResetCodeView.as_view(), name='reset-confirm-code'),
    path('reset-password/confirm-password/', ConfirmPasswordView.as_view(), name='reset-confirm-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/<int:pk>/', UserAccountAPIView.as_view(), name='user-account'),
    path('account/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-account-update'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
