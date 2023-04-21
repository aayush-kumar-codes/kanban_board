from django.db.utils import IntegrityError
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenRefreshView

from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenRefreshSerializer
from .utils import generate_tokens


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": f"{serializer.errors.keys()} is a required field",
            }, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data['password']

        if password != serializer.validated_data['confirm_password']:
            return Response(data={
                    "error": True,
                    "message": "Password and confirm password should match!"
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
        except IntegrityError:
            return Response(data={
                "error": True,
                "message": "Please enter correct email address.",
            }, status=status.HTTP_400_BAD_REQUEST)
            
        access_token, refresh_token = generate_tokens(user=user)

        response = {
            "error": False,
            "details": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": f"{serializer.errors.keys()} is a required field",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if not user:
            return Response(data={
                "error": True,
                "message": "Entered email or password is incorrect.",
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token, refresh_token = generate_tokens(user=user)

        response = {
            "error": False,
            "details": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
        return Response(response, status=status.HTTP_200_OK)
    

class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": "'refresh' is a required field"
            })

        response = super().post(request, *args, **kwargs)

        # Get the access token from the response
        access_token = response.data.get('access')

        custom_response = {
            "error": False,
            'access_token': access_token,
            'message': 'Token refreshed successfully',
        }
        # Return the custom response
        return Response(custom_response, status=response.status_code)
