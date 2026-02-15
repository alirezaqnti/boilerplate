from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Boilerplate JWT obtain serializer."""


class AuthenticationTokensSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
