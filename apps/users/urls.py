from django.urls import path

from apps.users import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path('confirm/', views.ConfirmEmailView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('reset-password-verify/', views.ConfirmCodeView.as_view()),
    path('reset_password_finish/', views.ConfirmPasswordView.as_view()),
    path('users-list/', views.UserListAPIView.as_view()),
    path('users-update/', views.UserUpdateAPIView.as_view(), name='user-update'),

    path('user-account/<int:pk>', views.UserAccountAPIView.as_view()),

]
