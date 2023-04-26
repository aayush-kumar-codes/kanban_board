from rest_framework import serializers


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20)
    confirm_password = serializers.CharField(required=True, max_length=20)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, max_length=300)
