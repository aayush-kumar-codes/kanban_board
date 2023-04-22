from django.urls import path

from .views import UserRegistrationView, UserLoginView, RefreshTokenView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view())
]
