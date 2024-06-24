"""All the serializers of the posts app"""

from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostSerializer(ModelSerializer):
    """Serializer for the Post model"""

    class Meta:
        """Necessary class for parents class functionality"""

        model = Post
        fields: str | list[str] = "__all__"
