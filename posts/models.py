"""All the models for the posts app"""

from typing import override

from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)
from accounts.models import User


class Post(Model):
    """Model to create each posts"""

    title: CharField = CharField(max_length=50)
    description: TextField = TextField()
    created: DateTimeField = DateTimeField(auto_now_add=True)
    author: ForeignKey = ForeignKey(User, on_delete=CASCADE, related_name="posts")

    @override
    def __str__(self) -> str:
        return str(self.title)
