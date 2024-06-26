"""All the serializers of the posts app"""

from typing import Any, override
from rest_framework.serializers import ModelSerializer, StringRelatedField
from posts.models import Post


class PostSerializer(ModelSerializer):
    """Serializer for the Post model"""

    author: StringRelatedField = StringRelatedField(read_only=True)

    @override
    def create(self, validated_data: Any) -> Any:
        return super().create(validated_data)

    class Meta:
        """Necessary class for parents class functionality"""

        model = Post
        fields: str | list[str] = "__all__"
