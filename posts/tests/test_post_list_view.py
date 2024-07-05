"""Running all the test for the PostList view"""

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from posts.tests.test_setup import TestSetUp


class TestPostList(TestSetUp):
    """Tests for the PostList View"""

    def test_post_creation(self) -> None:
        """Ensure the post can be created correctly"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        response: Response = self.client.post(path=self.posts_url, data=self.post_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), self.post_data.get("title"))
        self.assertEqual(
            response.data.get("description"), self.post_data.get("description")
        )
        self.assertEqual(response.data.get("author"), self.user_data.get("username"))

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin)
        response = self.client.post(path=self.posts_url, data=self.post_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), self.post_data.get("title"))
        self.assertEqual(
            response.data.get("description"), self.post_data.get("description")
        )
        self.assertEqual(response.data.get("author"), self.admin_user.get("username"))

    def test_post_creation_with_no_credentials(self) -> None:
        """Ensure the user must be authenticated to create new posts"""
        response: Response = self.client.post(path=self.posts_url, data=self.post_data)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

    def test_post_creation_with_other_credentials(self) -> None:
        """Ensure the user must be authenticated with the correct token to create new posts"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_key + "1f2g3asdf"
        )
        response: Response = self.client.post(path=self.posts_url, data=self.post_data)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data.get("detail")), "Invalid token.")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.post(path=self.posts_url, data=self.post_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), self.post_data.get("title"))
        self.assertEqual(
            response.data.get("description"), self.post_data.get("description")
        )
        self.assertEqual(response.data.get("author"), self.user_data2.get("username"))

    def test_post_list_with_credentials(self) -> None:
        """Ensure can display all the posts that were created before"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        posts_quantity: int = 7

        self._create_posts(posts_quantity)

        response: Response = self.client.get(path=self.posts_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), posts_quantity)

    def test_post_list_with_no_credentials(self) -> None:
        """Ensure can display all the posts that were created before even with no credentials"""
        posts_quantity: int = 4
        self._create_posts(posts_quantity)

        response: Response = self.client.get(path=self.posts_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), posts_quantity)

    def test_post_list_with_wrong_credentials(self) -> None:
        """Ensure cannot display all the posts due wrong token"""
        posts_quantity: int = 40
        self._create_posts(posts_quantity)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_key + "f3sa23-aks"
        )

        response: Response = self.client.get(path=self.posts_url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data.get("detail")), "Invalid token.")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.get(path=self.posts_url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), posts_quantity)
