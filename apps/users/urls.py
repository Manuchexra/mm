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
    path('register/', UserRegisterAPIView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password/confirm-code/', ConfirmResetCodeView.as_view()),
    path('reset-password/confirm-password/', ConfirmPasswordView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('account', UserAccountAPIView.as_view(), name='user-account'),
    path('account/update/<int:pk>/', UserUpdateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
