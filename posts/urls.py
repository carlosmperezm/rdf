"""Urls of the posts app"""

from django.urls import URLPattern, path
from posts.views import PostListView, PostDetailView

urlpatterns: list[URLPattern] = [
    path("", PostListView.as_view(), name="posts_list"),
    path("<int:id>", PostDetailView.as_view(), name="post_detail"),
]
