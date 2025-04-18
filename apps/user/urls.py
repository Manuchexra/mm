from django.urls import path
from .views import RegisterView, ProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import swagger_logout

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view()),
    path('logout/', swagger_logout, name='token_logout'),
]
