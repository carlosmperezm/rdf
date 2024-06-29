"""All the serializers of the posts app"""

from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    ManyRelatedField,
)
from posts.models import Post


class PostSerializer(ModelSerializer):
    """Serializer for the Post model"""

    author: StringRelatedField[Post] | ManyRelatedField = StringRelatedField(
        read_only=True
    )

    class Meta:
        """Necessary class for parents class functionality"""

        model = Post
        fields: str | list[str] = "__all__"
