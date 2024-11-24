from django.test import TestCase
from books.models import Book
from decimal import Decimal
from django.core.exceptions import ValidationError


class BookModelTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": Book.CoverType.HARD,
            "inventory": 10,
            "daily_price": Decimal("5.00"),
        }

    def test_book_creation(self):
        book = Book.objects.create(**self.valid_data)
        self.assertEqual(book.title, self.valid_data["title"])
        self.assertEqual(book.author, self.valid_data["author"])
        self.assertEqual(book.cover, self.valid_data["cover"])
        self.assertEqual(book.inventory, self.valid_data["inventory"])
        self.assertEqual(book.daily_price, self.valid_data["daily_price"])

    def test_book_invalid_inventory(self):
        self.valid_data["inventory"] = 0  # Invalid inventory
        book = Book(**self.valid_data)
        with self.assertRaises(ValidationError):
            book.full_clean()  # Triggers validation

    def test_book_invalid_daily_price(self):
        self.valid_data["daily_price"] = Decimal("0.00")  # Invalid price
        book = Book(**self.valid_data)
        with self.assertRaises(ValidationError):
            book.full_clean()  # Triggers validation

    def test_str_representation(self):
        book = Book.objects.create(**self.valid_data)
        expected_str = f"{book.title} by {book.author} ({book.get_cover_display()})"
        self.assertEqual(str(book), expected_str)
