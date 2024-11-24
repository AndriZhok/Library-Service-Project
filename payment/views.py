from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


@extend_schema_view(
    list=extend_schema(
        summary="List Payments",
        description="Retrieve a list of payments made by the authenticated user.",
        responses={200: PaymentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a Payment",
        description="Retrieve the details of a specific payment made by the authenticated user.",
        responses={200: PaymentSerializer},
    ),
    create=extend_schema(
        exclude=True,  # Payments are typically created automatically, not manually
    ),
    update=extend_schema(
        exclude=True,  # Updates to payments are typically not allowed
    ),
    partial_update=extend_schema(
        exclude=True,  # Partial updates to payments are not allowed
    ),
    destroy=extend_schema(
        exclude=True,  # Deleting payments is not allowed
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and managing payments.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter payments to only show those related to the authenticated user.
        """
        user = self.request.user
        return super().get_queryset().filter(borrowing__user=user)


@extend_schema(
    summary="Payment Success Page",
    description="Display a success message when a payment is completed successfully.",
    responses={200: "Оплата успішна. Дякуємо за використання нашої бібліотеки!"},
)
def payment_success(request):
    """
    Display a success message for completed payments.
    """
    return HttpResponse("Оплата успішна. Дякуємо за використання нашої бібліотеки!")


@extend_schema(
    summary="Payment Cancel Page",
    description="Display a cancellation message when a payment is cancelled.",
    responses={200: "Оплата скасована. Ви можете повторити спробу пізніше."},
)
def payment_cancel(request):
    """
    Display a cancellation message for payments.
    """
    return HttpResponse("Оплата скасована. Ви можете повторити спробу пізніше.")
