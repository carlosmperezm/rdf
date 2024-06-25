"""All the serializers for the accounts app"""

from typing import Any, override

from rest_framework.serializers import ModelSerializer

from accounts.models import User


class UserSerializer(ModelSerializer):
    """Serializer to serialize the user model"""

    class Meta:
        """Necessary class fot the parent class"""

        model = User
        fields: str | list[str] = "__all__"

    @override
    def create(self, validated_data: dict[str, Any] | Any) -> User:
        password: str = validated_data.pop("password")
        user: User = super().create(validated_data)
        user.set_password(raw_password=password)
        user.save()
        return user
