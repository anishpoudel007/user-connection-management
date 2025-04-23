from django.contrib.auth import get_user_model
from rest_framework import serializers

from connections.models import Connection
from connections.tasks import send_connection_notification

User = get_user_model()


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"
        read_only_fields = ("user_1", "user_2", "created_at", "updated_at")


class ConnectionCreateSerializer(serializers.Serializer):
    user_code = serializers.CharField()

    def validate_user_code(self, value):
        try:
            user = User.objects.get(user_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        self.context["to_user"] = user
        return value

    def validate(self, attrs):
        from_user = self.context["request"].user
        to_user = self.context.get("to_user")

        if from_user == to_user:
            raise serializers.ValidationError("You cannot connect to yourself.")

        if Connection.objects.filter(user_1=from_user, user_2=to_user).exists():
            raise serializers.ValidationError("Connection already exists.")

        return attrs

    def create(self, validated_data):
        from_user = self.context.get("request").user
        to_user = self.context.get("to_user")

        connection = Connection.objects.create(user_1=from_user, user_2=to_user)

        send_connection_notification.delay(
            connection_id=connection.id,
            sender_id=from_user.id,
            status=Connection.Status.PENDING,
        )

        return connection


class ConnectionUpdateSerializer(serializers.Serializer):
    connection_id = serializers.IntegerField(write_only=True)
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
                instance.id, self.context["request"].user.id, validated_data["status"]
            )
        except Exception as e:
            print(f"Celery task call failed: {e}")
        return instance
