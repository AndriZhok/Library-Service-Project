from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from datetime import date
import os
import requests
from dotenv import load_dotenv

from .models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)

load_dotenv()

TELEGRAM_API_URL = os.environ.get("TELEGRAM_URL")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def send_telegram_message(self, message):
        data = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(TELEGRAM_API_URL, data=data)
        if response.status_code != 200:
            raise Exception(f"Не вдалося відправити повідомлення: {response.text}")

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        elif user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        self.send_telegram_message(
            f"Вітаємо!!! Ви взяли книгу '{borrowing.book.title}'. Очікувана дата повернення: {borrowing.expected_return_date}."
        )

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request, pk=None):
        borrowing = get_object_or_404(Borrowing, pk=pk)
        serializer = BorrowingReturnSerializer(instance=borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()

        # Відправлення повідомлення про повернення книги
        self.send_telegram_message(
            f"Книга '{borrowing.book.title}' була успішно повернута. Дякуємо за вчасне повернення!"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
