from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    type = models.CharField(
        max_length=10, choices=PaymentType.choices, default=PaymentType.PAYMENT
    )
    borrowing = models.OneToOneField(
        "borrowing.Borrowing", on_delete=models.CASCADE, related_name="payment_info"
    )
    session_url = models.URLField(max_length=400)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )

    def __str__(self):
        return f"Payment: {self.type} | Status: {self.status} | Amount: ${self.money_to_pay}"
