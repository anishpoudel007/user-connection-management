from django.contrib.auth import get_user_model
from rest_framework import serializers

from connections.models import Connection

User = get_user_model()


class ConnectionCreateSerializer(serializers.Serializer):
    user_code = serializers.CharField()

    def validate_user_code(self, value):
        try:
            user = User.objects.get(user_code=value)
        except User.UserDoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        self.context["to_user"] = user
        return user

    def create(self, validated_data):
        from_user = self.context["request"].user
        to_user = validated_data["user_code"]

        if from_user == to_user:
            raise serializers.ValidationError("You cannot connect to yourself")

        connection, created = Connection.objects.get_or_create(
            user_1=from_user, user_2=to_user
        )

        if not created:
            raise serializers.ValidationError("Connection already exists.")

        return connection
