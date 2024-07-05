"""All tests for PostsForUser View"""

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED


from posts.tests.test_setup import TestSetUp


class TestPostsForUser(TestSetUp):
    """Test for Post For User View"""

    def test_get_posts_for_current_user(self) -> None:
        """Ensure the view can display all the posts of the current user"""
        posts_quantity: int = 4
        self._create_posts(posts_quantity)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        respnse: Response = self.client.get(path=self.post_for_this_user_url)

        self.assertEqual(respnse.status_code, HTTP_200_OK)
        self.assertEqual(len(respnse.data), posts_quantity)
        map(
            lambda post: self.assertEqual(
                post.get("author"), self.user_data.get("username")
            ),
            respnse.data,
        )

    def test_get_posts_for_current_user_with_no_credentials(self) -> None:
        """Ensure the view cannot display all the posts of the current user
        if the user is not authenticated"""
        posts_quantity: int = 1
        self._create_posts(posts_quantity)
        respnse: Response = self.client.get(path=self.post_for_this_user_url)

        self.assertEqual(respnse.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(respnse.data.get("detail")),
            "Authentication credentials were not provided.",
        )

    def test_get_posts_for_current_user_with_wrong_token(self) -> None:
        """Ensure the view cannot display all the posts of the current user
        if the user insert the wrong token"""
        posts_quantity: int = 1
        self._create_posts(posts_quantity)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "as5fds3")
        respnse: Response = self.client.get(path=self.post_for_this_user_url)

        self.assertEqual(respnse.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(respnse.data.get("detail")),
            "Invalid token.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.get(path=self.post_for_this_user_url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(respnse.data), posts_quantity)
        map(
            lambda post: self.assertEqual(
                post.get("author"), self.user_data.get("username")
            ),
            respnse.data,
        )
