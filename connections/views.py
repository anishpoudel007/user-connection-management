from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from connections.models import Connection
from connections.serializer import (
    ConnectionCreateSerializer,
    ConnectionSerializer,
    ConnectionUpdateSerializer,
)


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


class UserConnectionRequestUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, connection_id):
        connection = get_object_or_404(Connection, id=connection_id)

        data = request.data.copy()
        data["connection_id"] = connection_id

        serializer = ConnectionUpdateSerializer(
            instance=connection, data=data, context={"request": request}
        )

        if serializer.is_valid():
            instance = serializer.save()

            connection_serializer = ConnectionSerializer(
                instance=instance,
            )
            return Response(connection_serializer.data)
        return Response({"errors": serializer.errors})
