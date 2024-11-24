from decimal import Decimal
from django.db import models
from django.db.models import F
from books.models import Book
from payment.models import Payment


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="borrowings"
    )
    payment = models.OneToOneField(
        "payment.Payment",
        on_delete=models.CASCADE,
        related_name="borrowing_item",
        null=True,
        blank=True,
    )

    def calculate_total_price(self) -> Decimal:
        """Calculate the total price for borrowing based on the duration and daily price."""
        duration = (self.expected_return_date - self.borrow_date).days
        daily_price = getattr(self.book, "daily_price", None)

        # Ensure daily_price exists and is a valid number
        if daily_price is None:
            raise ValueError(
                f"The book '{self.book.title}' does not have a daily_price."
            )
        return Decimal(duration * daily_price)

    def __str__(self) -> str:
        return f"Borrowing: {self.book.title} by {self.user.username}"
