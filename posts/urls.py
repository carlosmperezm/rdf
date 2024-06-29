"""Urls of the posts app"""

from django.urls import URLPattern, path
from posts.views import PostListView, PostDetailView, PostsForUserView

urlpatterns: list[URLPattern] = [
    path("", PostListView.as_view(), name="posts_list"),
    path("<int:post_id>", PostDetailView.as_view(), name="post_detail"),
    path("for_this_user/", PostsForUserView.as_view(), name="posts_for_this_user"),
]
