"""The accounts app logic """

from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

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


class LoginView(APIView):
    """Class to authenticate a user"""

    def post(self, request: Request) -> Response:
        """Method to log in a user"""
        password: str | None = request.data.get("password")
        email: str | None = request.data.get("email")
        user: AbstractBaseUser | None = authenticate(email=email, password=password)
        if user is not None:
            token: Token | None = Token.objects.get(user=user)
            data: dict[str, Any] = {
                "message": "Login successfully",
                "token": str(token.key),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        response: dict[str, Any] = {"message": "Error trying to validate the user"}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request) -> Response:
        """Get information about the current user"""
        data: dict[str, Any] = {"user": str(request.user), "token": str(request.auth)}

        return Response(data=data, status=status.HTTP_200_OK)
