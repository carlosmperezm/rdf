"""Configs to apply before tests get run """

from typing import override
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

        self.client.post(
            path="http://localhost:8000/auth/signup/",
            data=self.user_data,
        )

        self.token_key: str = self.client.post(
            path="http://localhost:8000/auth/login/", data=self.user_data
        ).data.get("token")
        return super().setUp()

    @override
    def tearDown(self) -> None:
        return super().tearDown()
