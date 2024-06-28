"""The permisions of the posts app"""

from typing import override
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from posts.models import Post


class IsAuthorOrReadOnly(BasePermission):
    """Verify if the user is the author or not, if he is... the user can modify his own posts
    Otherwise only can read
    """

    @override
    def has_object_permission(
        self, request: Request, _view: APIView, obj: Post
    ) -> bool:
        return bool(request.method in SAFE_METHODS or request.user == obj.author)
