"""The accounts app logic """

from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer


class SignUpView(APIView):
    """Class to create a new user"""

    def post(self, request: Request) -> Response:
        """Create a new user"""
        serializer: UserSerializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data: dict[str, Any] = serializer.data.copy()
            user_data.pop("password")
            return Response(data=user_data, status=status.HTTP_201_CREATED)
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

        response: dict[str, Any] = {"message": "Error: Email or password are incorrect"}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request) -> Response:
        """Get information about the current user"""
        data: dict[str, Any] = {"user": str(request.user), "token": str(request.auth)}

        return Response(data=data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    """View to manage all the User info"""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Show all the user's information"""
        user: AbstractBaseUser | AnonymousUser = request.user
        serializer: UserSerializer = UserSerializer(instance=user)
        user_data: dict[str, Any] = serializer.data.copy()
        user_data.pop("password")
        return Response(data=user_data, status=status.HTTP_200_OK)
