from typing import override, Any
from django.db.models import CharField, EmailField, DateField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    """Class to manage the User"""

    def create_user(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: dict[str, Any]
    ) -> AbstractUser:
        """Create a new user"""
        user: AbstractUser = self.model(
            email=self.normalize_email(email), username=username, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: Any
    ) -> AbstractUser:
        """Create a Super User"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super user has to have is_staff being True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super user has to have is_superuser being True")
        return self.create_user(
            email=email, username=username, password=password, **extra_fields
        )


class User(AbstractUser):
    """User model to create each user"""

    email: EmailField = EmailField(
        verbose_name="email address", max_length=100, unique=True
    )
    username: CharField = CharField(max_length=40)
    date_of_birth: DateField = DateField(null=True)
    name: CharField = CharField(max_length=50, null=True)
    last_name: CharField = CharField(max_length=200, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]

    @override
    def __str__(self) -> str:
        return str(self.username)
