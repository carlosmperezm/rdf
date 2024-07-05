"""File to manage of the logic and functionalities of the posts app"""

from typing import Iterable, Any, override

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db.models import QuerySet

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.serializers import BaseSerializer

from posts.serializer import PostSerializer
from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly


class PostListView(APIView):
    """View to manage get the post and create a new ones"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, _request: Request) -> Response:
        """Return all the posts"""
        posts: Iterable = Post.objects.all()
        serializer: PostSerializer = PostSerializer(instance=posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """create a new post"""
        data: dict[str, Any] = request.data
        user: AbstractBaseUser | AnonymousUser = request.user

        serializer: PostSerializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """View for each post"""

    permission_classes = [IsAdminUser | IsAuthorOrReadOnly]

    def get(self, request: Request, post_id: int) -> Response:
        """Get one post"""
        post: Post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        serializer: PostSerializer = PostSerializer(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, post_id: int) -> Response:
        """Update a post"""
        data: dict[str, Any] = request.data
        post: Post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        serializer: PostSerializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, post_id: int) -> Response:
        """Delete a post"""
        post: Post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        response: dict[str, str] = {"Message": "Deleted"}
        return Response(data=response, status=status.HTTP_200_OK)


class PostsForUserView(GenericAPIView):
    """Manage all the posts created by the current user"""

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @override
    def get_queryset(self) -> QuerySet:
        user: AbstractBaseUser | AnonymousUser = self.request.user
        return Post.objects.filter(author=user)

    def get(self, _request: Request) -> Response:
        """Get all the posts created by the authenticated user"""
        posts: QuerySet = self.get_queryset()
        serializer: PostSerializer | BaseSerializer = self.get_serializer_class()(
            instance=posts, many=True
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)
