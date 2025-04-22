from django.contrib.auth import get_user_model
from django.utils import choices
from rest_framework import serializers, status

from connections.models import Connection
from connections.tasks import send_connection_notification

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

        send_connection_notification.delay(
            connection_id=connection.id,
            sender_id=from_user.id,
            status=Connection.Status.PENDING,
        )

        return connection


class ConnectionUpdateSerializer(serializers.Serializer):
    connection_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Connection.Status.choices)

    def validate_connection_id(self, value):
        try:
            connection = Connection.objects.get(id=value)
        except Connection.DoesNotExist:
            raise serializers.ValidationError("Connection does not exist.")
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data["status"]
        instance.save()

        try:
            send_connection_notification.delay(
                instance.id, self.context["request"].user.id, instance.status
            )
        except Exception as e:
            print(f"Celery task call failed: {e}")
        # send_connection_notification.delay(
        #     connection_id=instance.id,
        #     sender_id=self.context["request"].user.id,
        #     status=validated_data["status"],
        # )
        return instance
