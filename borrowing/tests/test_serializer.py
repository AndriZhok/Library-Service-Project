from datetime import date, timedelta
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class BorrowingSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
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

    def test_borrowing_return_serializer_success(self):
        self.borrowing.actual_return_date = None
        self.borrowing.save()
        data = {"actual_return_date": date.today()}
        serializer = BorrowingReturnSerializer(instance=self.borrowing, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        borrowing = serializer.save()
        self.assertEqual(borrowing.actual_return_date, date.today())
        self.assertEqual(self.book.inventory, 6)  # Inventory should increment

    def test_borrowing_return_serializer_already_returned(self):
        self.borrowing.actual_return_date = date.today()
        self.borrowing.save()
        data = {"actual_return_date": date.today()}
        serializer = BorrowingReturnSerializer(instance=self.borrowing, data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            str(context.exception.detail["non_field_errors"][0]),
            "This borrowing has already been returned.",
        )
