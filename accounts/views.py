"""The accounts app logic """

from typing import Any

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import UserSerializer


class SignUpView(APIView):
    """Class to create a new user"""

    def post(self, request: Request) -> Response:
        """Create a new user"""
        data: dict[str, Any] = request.data
        serializer: UserSerializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """Class to authenticate a user"""
