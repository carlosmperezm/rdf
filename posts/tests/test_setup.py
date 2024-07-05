"""Configs to apply before tests get run """

from typing import override, Any
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    """Class to setup configs before the tests start running"""

    @override
    def setUp(self) -> None:
        self.posts_url: str = reverse("posts_list")
        self.post_detail_url: str = reverse("post_detail", kwargs={"post_id": 1})
        self.post_for_this_user_url: str = reverse("posts_for_this_user")
        self.post_data: dict[str, str] = {
            "title": "This is my test post",
            "description": "Description of the test post",
        }
        self.user_data: dict[str, str] = {
            "email": "user@test.com",
            "username": "usertest",
            "password": "password1234test",
        }
        self.user_data2: dict[str, str] = {
            "email": "user2@test2.com",
            "username": "user2",
            "password": "user2password",
        }
        self.admin_user: dict[str, Any] = {
            "email": "admin@test.com",
            "username": "admin",
            "password": "adminpassword123",
            "is_admin": True,
            "is_staff": True,
        }

        self.client.post(
            path=reverse("signup"),
            data=self.user_data,
        )
        self.client.post(
            path=reverse("signup"),
            data=self.user_data2,
        )
        self.client.post(path=reverse("signup"), data=self.admin_user)

        self.token_key: str = self.client.post(
            path=reverse("login"), data=self.user_data
        ).data.get("token")

        self.token_key2: str = self.client.post(
            path=reverse("login"), data=self.user_data2
        ).data.get("token")

        self.token_admin: str = self.client.post(
            path=reverse("login"), data=self.admin_user
        ).data.get("token")

        return super().setUp()

    @override
    def tearDown(self) -> None:
        return super().tearDown()

    def _create_posts(self, posts_quantity: int) -> None:
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        for _ in range(posts_quantity):
            self.client.post(path=self.posts_url, data=self.post_data)
        self.client.credentials()
