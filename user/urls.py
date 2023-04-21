from django.urls import path

from .views import UserRegistrationView, UserLoginView, RefreshTokenView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh')
]
