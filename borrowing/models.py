from django.db import models

from books.models import Book


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

    def __str__(self) -> str:
        return f"Borrowing: {self.book.title} by {self.user.username}"
