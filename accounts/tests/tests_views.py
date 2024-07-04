"""Tests for the Views"""

from typing import Any
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response

from accounts.tests.test_setup import TestSetUP
from accounts.models import User
from accounts.serializers import UserSerializer


class TestSignup(TestSetUP):
    """Tests for Signup View"""

    def test_signup(self) -> None:
        """Test the register a user with the correct information"""
        response: Response = self.client.post(
            path=self.signup_url, data=self.user_data, format="json"
        )
        user: User = User.objects.get(email=self.user_data.get("email"))

        serializer: UserSerializer = UserSerializer(instance=user)
        serializer_data: dict[str, Any] = serializer.data.copy()
        serializer_data.pop("password")

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(serializer_data, response.data)

    def test_signup_with_no_valid_data(self) -> None:
        """Test the register a user with information missing"""
        copy_data: dict[str, str] = self.user_data.copy()
        copy_data.pop("username")
        response: Response = self.client.post(path=self.signup_url, data=copy_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class TestLogin(TestSetUP):
    """Test for Login View"""

    def test_login(self) -> None:
        """Testing user login with the correct credentials"""
        self.client.post(path=self.signup_url, data=self.user_data, format="json")

        response: Response = self.client.post(
            path=self.login_url,
            data=self.user_data,
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Login successfully")

    def test_login_with_wrong_credentials(self) -> None:
        """Testing if the user insert an incorrect password or email"""
        self.client.post(path=self.signup_url, data=self.user_data, format="json")

        copy_data: dict[str, str] = self.user_data.copy()
        copy_data["password"] = "mypassword#123"

        response: Response = self.client.post(path=self.login_url, data=copy_data)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("message"), "Error: Email or password are incorrect"
        )


class TestUserInfo(TestSetUP):
    """UserInfo View Tests"""

    def _get_token(self) -> str:
        self.client.post(path=self.signup_url, data=self.user_data, format="json")
        token_key: str = self.client.post(
            path=self.login_url, data=self.user_data, format="json"
        ).data.get("token")
        return token_key

    def test_userinfo_with_correct_credentials(self) -> None:
        """Test if the view send the correct data of the user"""
        token_key: str = self._get_token()

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)

        response: Response = self.client.get(path=self.userinfo_url, format="json")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("email"), self.user_data.get("email"))
        self.assertEqual(response.data.get("username"), self.user_data.get("username"))

    def test_userinfo_with_wrong_token(self) -> None:
        """Test if the view validate the token if is valid or not"""
        token_key: str = self._get_token() + "asdfasdf"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        response: Response = self.client.get(
            path=self.userinfo_url, data=self.user_data, format="json"
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data.get("detail")), "Invalid token.")

    def test_userinfo_with_no_token(self) -> None:
        """Tests if the view can check if no authentication were not provided"""
        self._get_token()

        response: Response = self.client.get(
            path=self.userinfo_url, data=self.user_data, format="json"
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail").code, "not_authenticated")
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )
