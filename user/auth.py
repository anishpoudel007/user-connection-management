import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, exceptions

from project import settings


User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token_str = auth_header.split(" ")[-1]

        try:
            payload = jwt.decode(
                token_str, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid Token.")

        try:
            user = User.objects.get(username=payload["username"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

        return (user, None)
