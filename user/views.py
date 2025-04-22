import datetime
import jwt
from django.contrib.auth import authenticate
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from project import settings
from user.models import User
from user.serializer import (
    LoginSerializer,
    UserRegisterSerializer,
    UserSearchSerializer,
    UserSerializer,
)


class UserSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        company_name = self.request.query_params.get("company_name")
        email = self.request.query_params.get("email")
        contact_number = self.request.query_params.get("contact_number")

        queryset = User.objects.all()

        if name:
            queryset = queryset.filter(username__icontains=name)
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if contact_number:
            queryset = queryset.filter(contact_number__icontains=contact_number)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user = authenticate(
                request,
                username=validated_data["username"],
                password=validated_data["password"],
            )

            if user is not None:
                # generate JWT Token
                payload = {
                    "username": user.username,
                    "exp": datetime.datetime.now(datetime.timezone.utc)
                    + settings.JWT_ACCESS_TOKEN_LIFETIME,
                    "iat": datetime.datetime.now(),
                }

                token = jwt.encode(
                    payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
                )

                return Response(
                    {
                        "access_token": token,
                        "user": {
                            "user_code": user.user_code,
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
