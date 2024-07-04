"Tests for the models of the accounts app"
from typing import override
from django.test import TestCase
from accounts.models import User


class UserTest(TestCase):
    """Tests for the model user"""

    @override
    def setUp(self) -> None:
        self.obj: User = User.objects.create(
            username="usertest", email="user@test.com", password="passwordtest1234"
        )
        return super().setUp()

    def test_model_fields(self) -> None:
        """Tests the fields of the model"""
        self.assertEqual(self.obj.username, "usertest")
        self.assertEqual(self.obj.email, "user@test.com")
        self.assertEqual(self.obj.password, "passwordtest1234")
