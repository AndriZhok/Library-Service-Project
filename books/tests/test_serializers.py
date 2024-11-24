from django.test import TestCase
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer, BookDetailSerializer
from decimal import Decimal


class BookSerializerTests(TestCase):
    def setUp(self):
        # Create a sample book
        self.book = Book.objects.create(
            title="Sample Book",
            author="Author Name",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_price=Decimal("5.00"),
        )

    def test_book_serializer(self):
        # Serialize the book
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "title": "Sample Book",
            "author": "Author Name",
            "cover": "HARD",
            "inventory": 10,
            "daily_price": "5.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_list_serializer(self):
        # Serialize the book using BookListSerializer
        serializer = BookListSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "Author Name",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_detail_serializer(self):
        # Serialize the book using BookDetailSerializer
        serializer = BookDetailSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "Author Name",
            "cover": "HARD",
            "inventory": 10,
            "daily_price": "5.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_serializer_validation(self):
        # Test serializer validation with valid data
        valid_data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_price": "3.50",
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "New Book")

    def test_book_serializer_invalid_data(self):
        # Test serializer validation with invalid data
        invalid_data = {
            "title": "",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 0,  # Invalid inventory
            "daily_price": "-5.00",  # Invalid daily price
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("inventory", serializer.errors)
        self.assertIn("daily_price", serializer.errors)
