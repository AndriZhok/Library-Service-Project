from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(borrowing__user=user)


def payment_success(request):
    return HttpResponse("Оплата успішна. Дякуємо за використання нашої бібліотеки!")


def payment_cancel(request):
    return HttpResponse("Оплата скасована. Ви можете повторити спробу пізніше.")
