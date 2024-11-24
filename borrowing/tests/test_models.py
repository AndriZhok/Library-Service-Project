from decimal import Decimal
from datetime import date
from django.test import TestCase
from books.models import Book
from user.models import User
from borrowing.models import Borrowing


class BorrowingModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

        # Create a book with a valid daily price
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_price=Decimal("10.00"),
        )

    def test_calculate_total_price_valid(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )
        total_price = borrowing.calculate_total_price()
        self.assertEqual(total_price, Decimal("50.00"))  # 5 days * 10.00 daily price

    def test_calculate_total_price_missing_daily_price(self):
        # Simulate a book with a missing daily price by setting it in memory
        self.book.daily_price = None

        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )

        with self.assertRaises(ValueError) as context:
            borrowing.calculate_total_price()

        self.assertEqual(
            str(context.exception),
            f"The book '{self.book.title}' does not have a daily_price.",
        )

    def test_calculate_total_price_zero_days(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 20),  # Same day
            book=self.book,
            user=self.user,
        )
        total_price = borrowing.calculate_total_price()
        self.assertEqual(total_price, Decimal("0.00"))  # 0 days

    def test_calculate_total_price_negative_days(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 25),
            expected_return_date=date(2024, 11, 20),  # Return date before borrow date
            book=self.book,
            user=self.user,
        )
        total_price = borrowing.calculate_total_price()
        self.assertEqual(total_price, Decimal("-50.00"))  # -5 days * 10.00 daily price

    def test_str_representation(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )
        self.assertEqual(
            str(borrowing), f"Borrowing: {self.book.title} by {self.user.username}"
        )
