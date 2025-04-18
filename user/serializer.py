import uuid

from .models import User
from rest_framework import serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "user_code": {"read_only": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user_code = uuid.uuid4().hex

        print(validated_data)
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            contact_number=validated_data["contact_number"],
            company_name=validated_data["company_name"],
            industry=validated_data["industry"],
            user_code=user_code,
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
