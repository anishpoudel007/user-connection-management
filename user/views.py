from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny

from user.serializer import UserRegisterSerializer

import uuid


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            user_code = uuid.uuid4().hex

            # print(validated_data)
            serializer.save()

            return Response(validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
