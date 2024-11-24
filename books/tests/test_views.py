from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from books.models import Book
from decimal import Decimal

User = get_user_model()


class BookListViewTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="password",
        )

        # Create some books
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_price=Decimal("5.00"),
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            cover=Book.CoverType.SOFT,
            inventory=5,
            daily_price=Decimal("3.50"),
        )

        # Generate tokens
        self.user_token = AccessToken.for_user(self.user)
        self.admin_token = AccessToken.for_user(self.admin_user)

    def test_list_books_as_anonymous_user(self):
        response = self.client.get("/book/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_books_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get("/book/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_as_anonymous_user(self):
        response = self.client.get(f"/book/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_retrieve_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(f"/book/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_as_anonymous_user(self):
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_price": Decimal("6.00"),
        }
        response = self.client.post("/book/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_price": Decimal("6.00"),
        }
        response = self.client.post("/book/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_price": Decimal("6.00"),
        }
        response = self.client.post("/book/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_update_book_as_anonymous_user(self):
        data = {"title": "Updated Book"}
        response = self.client.put(f"/book/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {"title": "Updated Book"}
        response = self.client.put(f"/book/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "Updated Book",
            "author": self.book1.author,
            "cover": self.book1.cover,
            "inventory": self.book1.inventory,
            "daily_price": self.book1.daily_price,
        }
        response = self.client.put(f"/book/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_delete_book_as_anonymous_user(self):
        response = self.client.delete(f"/book/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.delete(f"/book/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(f"/book/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
