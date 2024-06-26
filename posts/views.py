"""File to manage of the logic and functionalities of the posts app"""

from typing import Iterable, Any

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from posts.serializer import PostSerializer

from posts.models import Post


class PostListView(APIView):
    """View to manage get the post and create a new ones"""

    permission_classes = [IsAuthenticated]

    def get(self, _request: Request) -> Response:
        """Return all the posts"""
        posts: Iterable = Post.objects.all()
        serializer: PostSerializer = PostSerializer(instance=posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """create a new post"""
        data: dict[str, Any] = request.data
        serializer: PostSerializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """View for each post"""

    def get(self, request: Request, post_id: int) -> Response:
        """Get one post"""
        post: Post = get_object_or_404(Post, pk=post_id)
        user: AbstractBaseUser | AnonymousUser = request.user

        if post.author.pk != user.pk:
            permission_error: dict[str, Any] = {
                "error": "You do not have enough permissions to retrieve this post "
            }
            return Response(data=permission_error, status=status.HTTP_401_UNAUTHORIZED)

        serializer: PostSerializer = PostSerializer(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, post_id: int) -> Response:
        """Update a post"""
        data: dict[str, Any] = request.data
        post: Post = get_object_or_404(Post, pk=post_id)
        user: AbstractBaseUser | AnonymousUser = request.user

        if post.author.pk != user.pk:
            permission_error: dict[str | Any] = {
                "error": "You do not have enough permissions to update this posts"
            }
            return Response(data=permission_error, status=status.HTTP_401_UNAUTHORIZED)

        serializer: PostSerializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, post_id: int) -> Response:
        """Delete a post"""
        post: Post = get_object_or_404(Post, pk=post_id)
        user: AbstractBaseUser | AnonymousUser = request.user

        if post.author.pk != user.pk:
            permission_error: dict[str | Any] = {
                "error": "You do not have enough permissions to delete this posts"
            }
            return Response(data=permission_error, status=status.HTTP_401_UNAUTHORIZED)

        post.delete()
        response: dict[str, str] = {"Message": "Deleted"}
        return Response(data=response, status=status.HTTP_200_OK)
