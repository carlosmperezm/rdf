"""Tests for the PostDetail View"""

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from posts.tests.test_setup import TestSetUp


class TestPostDetail(TestSetUp):
    """Tests for Post Detail View"""

    def test_get_post_by_id(self) -> None:
        """Ensure the view show the correct post"""
        posts_quantity: int = 3
        self._create_posts(posts_quantity)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)

        response: Response = self.client.get(path=self.post_detail_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("title"), self.post_data.get("title"))
        self.assertEqual(
            response.data.get("description"), self.post_data.get("description")
        )
        self.assertEqual(response.data.get("author"), self.user_data.get("username"))

    def test_get_post_by_wrong_id(self) -> None:
        """Ensure the view show 404 error when no posts were found with that id"""
        self._create_posts(3)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)

        response: Response = self.client.get(
            path=self.post_detail_url.replace("1", "5")
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            str(response.data.get("detail")), "No Post matches the given query."
        )

    def test_get_post_by_id_with_no_credentials(self) -> None:
        """Ensure the view show the correct post even with no credentials provided"""
        self._create_posts(100)

        response: Response = self.client.get(
            path=self.post_detail_url.replace("1", "100")
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.post_data.get("title"))
        self.assertEqual(
            response.data.get("description"), self.post_data.get("description")
        )
        self.assertEqual(response.data.get("author"), self.user_data.get("username"))

    def test_get_post_by_wrong_credentials(self) -> None:
        """Ensure the view do not allow to show any data if the user insert the wrond token"""
        self._create_posts(3)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "asdf2s" + self.token_key)

        response: Response = self.client.get(path=self.post_detail_url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data.get("detail")), "Invalid token.")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.get(path=self.post_detail_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_update_post(self) -> None:
        """Ensure the view update correctly the post"""
        self._create_posts(2)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        updated_data: dict[str, str] = {
            "title": "New title updated",
            "description": "Updated description",
        }
        response: Response = self.client.put(
            path=self.post_detail_url, data=updated_data
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("title"), updated_data.get("title"))
        self.assertEqual(
            response.data.get("description"), updated_data.get("description")
        )

    def test_update_post_by_wrong_id(self) -> None:
        """Ensure the the view send an not found if the id is wrong"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)
        updated_data: dict[str, str] = {
            "title": "New title updated",
            "description": "Updated description",
        }

        self.post_detail_url = self.post_detail_url.replace("1", "3")

        response: Response = self.client.put(
            path=self.post_detail_url, data=updated_data
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            str(response.data.get("detail")), "No Post matches the given query."
        )

    def test_update_post_with_no_credentials(self) -> None:
        """Ensure the view not update the post without the credentials"""
        self._create_posts(2)
        updated_data: dict[str, str] = {
            "title": "New title updated",
            "description": "Updated description",
        }
        response: Response = self.client.put(
            path=self.post_detail_url, data=updated_data
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

    def test_update_post_with_wrong_credentials(self) -> None:
        """Ensure the view not update the post with not correct the credentials"""
        self._create_posts(1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "xdxd")
        updated_data: dict[str, str] = {
            "title": "New title updated",
            "description": "Updated description",
        }
        response: Response = self.client.put(
            path=self.post_detail_url, data=updated_data
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Invalid token.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.put(path=self.post_detail_url, data=updated_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            str(response.data.get("detail")),
            "You do not have permission to perform this action.",
        )

    def test_delete_post(self) -> None:
        """Test the view delete correctly the post"""
        posts_quantity: int = 4
        self._create_posts(posts_quantity)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)

        self.post_detail_url = self.post_detail_url.replace("1", "3")

        response: Response = self.client.delete(path=self.post_detail_url)
        posts: Response = self.client.get(path=self.posts_url)
        post_deleted: int = self.client.get(path=self.post_detail_url).status_code

        self.assertEqual(post_deleted, HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(posts.data), posts_quantity - 1)

    def test_delete_post_by_wrong_id(self) -> None:
        """Test the view send an error if the post does not exit"""
        posts_quantity: int = 4
        self._create_posts(posts_quantity)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key)

        self.post_detail_url = self.post_detail_url.replace("1", "5")

        response: Response = self.client.delete(path=self.post_detail_url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            str(response.data.get("detail")), "No Post matches the given query."
        )

    def test_delete_post_with_no_credentials(self) -> None:
        """Ensure the view no do not delete if no credetials were not provided"""
        posts_quantity: int = 1
        self._create_posts(posts_quantity)

        response: Response = self.client.delete(path=self.post_detail_url)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

    def test_delete_post_with_wrong_credentials(self) -> None:
        """Ensure the view no do not delete if no correct credentials were provided"""
        posts_quantity: int = 1
        self._create_posts(posts_quantity)

        self.client.credentials(HTTP_AUTHORIZATION="Token as")
        response: Response = self.client.delete(path=self.post_detail_url)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Invalid token.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_key2)
        response = self.client.delete(path=self.post_detail_url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            str(response.data.get("detail")),
            "You do not have permission to perform this action.",
        )
