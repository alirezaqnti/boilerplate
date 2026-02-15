from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class HatchupJWTAuthentication(JWTAuthentication):
    def authenticate(self, request) -> Optional[Tuple]:
        auth_header = request.META.get("Authorization", "") or request.META.get(
            "authorization", ""
        )
        if not auth_header:
            return None

        try:
            header = auth_header.split()
            if not header or len(header) != 2:
                raise AuthenticationFailed("Invalid authorization header format.")

            raw_token = header[1]
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user_object(validated_token)
            request.user = user
            return user, validated_token
        except TokenError:
            raise AuthenticationFailed("Invalid token")
        except InvalidToken:
            raise AuthenticationFailed("Token is invalid or expired")
        except AuthenticationFailed:
            raise
        except Exception:
            raise AuthenticationFailed("Authentication failed")

    def get_user_object(self, validated_token):
        decoded_payload = validated_token.payload

        try:
            user = User.objects.get(id=decoded_payload.get("user_id"), is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        # Keep role-based validation logic for deployments that include role claims.
        role = decoded_payload.get("role")
        if not role:
            return user

        user_types = getattr(user, "user_types", None)
        if user_types is None:
            return user

        if role == "staff":
            if not user_types.filter(name="staff").exists():
                raise AuthenticationFailed("Staff user not found")
        elif role == "customer":
            if not user_types.filter(name="customer").exists():
                raise AuthenticationFailed("Customer user not found")
        else:
            raise AuthenticationFailed("Invalid user role")

        return user


class HatchupAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = HatchupJWTAuthentication
    name = "Hatchup_auth"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix=self.target.keyword,
        )
