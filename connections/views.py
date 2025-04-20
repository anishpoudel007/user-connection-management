from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from connections.serializer import ConnectionCreateSerializer


class UserConnectionRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConnectionCreateSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            connection = serializer.save()
            return Response(
                {
                    "message": "Connection request sent.",
                    "status": connection.status,
                    "created_at": connection.created_at,
                }
            )
        return Response({"message": "user-connection-request"})
