from typing import override

from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUP(APITestCase):
    @override
    def setUp(self) -> None:
        self.signup_url: str = reverse("signup")
        self.login_url: str = reverse("login")
        self.userinfo_url: str = reverse("userinfo")
        self.user_data: dict[str, str] = {
            "email": "user@test.com",
            "username": "usertest",
            "password": "passwordtest",
        }

        return super().setUp()

    @override
    def tearDown(self) -> None:
        return super().tearDown()
