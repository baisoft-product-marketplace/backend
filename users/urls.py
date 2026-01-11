from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # Obtain access and refresh tokens
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),

    # Refresh access token using refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

