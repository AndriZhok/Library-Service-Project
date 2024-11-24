import os
from datetime import date, timedelta
from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from unittest.mock import patch

from books.models import Book
from borrowing.models import Borrowing
from django.contrib.auth import get_user_model

User = get_user_model()


class BorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="password"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_price=Decimal("1.50"),
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=5),
            book=self.book,
            user=self.user,
        )
        self.user_token = AccessToken.for_user(self.user)
        self.admin_token = AccessToken.for_user(self.admin_user)

    def test_list_borrowings_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_borrowing_as_anonymous_user(self):
        data = {
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=3),
            "book": self.book.id,
        }
        response = self.client.post(reverse("borrowing:borrowing-list"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_borrowing_as_anonymous_user(self):
        response = self.client.get(
            reverse("borrowing:borrowing-detail", args=[self.borrowing.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_borrowing_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(
            reverse("borrowing:borrowing-detail", args=[self.borrowing.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)

    def test_return_borrowing_as_anonymous_user(self):
        data = {"actual_return_date": date.today()}
        response = self.client.post(
            reverse("borrowing:borrowing-return-borrowing", args=[self.borrowing.id]),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
