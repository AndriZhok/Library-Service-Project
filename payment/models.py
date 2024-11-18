from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=7, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    type = models.CharField(max_length=7, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(
        max_digits=10,  # Adjust for larger sums
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    def __str__(self) -> str:
        return f"Payment: {self.type} ({self.status}) for {self.borrowing}"
