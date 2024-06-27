"""All the serializers for the accounts app"""

from typing import Any, override

from django.db.models import Model

from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework.authtoken.models import Token

from accounts.models import User


class UserSerializer(ModelSerializer):
    """Serializer to serialize the user model"""

    posts: StringRelatedField[Model] = StringRelatedField(many=True, read_only=True)

    class Meta:
        """Necessary class fot the parent class"""

        model = User
        fields: str | list[str] = "__all__"

    @override
    def create(self, validated_data: dict[str, Any] | Any) -> User:
        password: str | None = validated_data.pop("password", None)
        user: User = super().create(validated_data)
        user.set_password(raw_password=password)
        user.save()

        Token.objects.create(user=user)

        return user
