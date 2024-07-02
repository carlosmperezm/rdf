"""All the tests for the posts app"""

from typing import override

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from accounts.models import User


# Create your tests here.
class PostListTest(APITestCase):
    """
    Test the PostListView when as GET method returns a list of all the posts
    and as POST method create a new post
    """

    def _singup(self) -> None:
        self.client.post(
            reverse("signup"),
            {
                "email": "bob@test.com",
                "password": "12345678",
                "username": "bob test",
            },
            format="json",
        )

    def _authenticate(self) -> str:
        response = self.client.post(
            reverse("login"),
            {"email": "bob@test.com", "password": "12345678"},
            format="json",
        )
        return response.data.get("token")

    @override
    def setUp(self) -> None:
        self._singup()
        self.token: str = self._authenticate()
        self.user: User = User.objects.get(email="bob@test.com")
        self.url: str = reverse("posts_list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_post_list(self) -> None:
        """Test when a GET petition is made the view returns all the posts"""
        response: Response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_creation(self) -> None:
        """Test when a POST petition is made"""
        data: dict = {
            "title": "My post title",
            "description": "This is my post description",
        }
        response: Response = self.client.post(path=self.url, data=data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
