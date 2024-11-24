import os
import stripe
import requests

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv

from payment.models import Payment
from .models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from .tasks import send_telegram_message

load_dotenv()

TELEGRAM_API_URL = os.environ.get("TELEGRAM_URL")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
stripe.api_key = os.environ.get("STRIPE_API_KEY")


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

        # Якщо платіж ще не створено
        payment = Payment.objects.create(
            borrowing=borrowing,
            money_to_pay=borrowing.calculate_total_price(),
            status="PENDING",
            type="PAYMENT",
        )

        # Створення платіжної сесії Stripe
        session = self.create_payment_session(borrowing)

        payment.session_id = session["id"]
        payment.session_url = session["url"]
        payment.save()

        self.payment_url = session["url"]

    def create_payment_session(self, borrowing):

        success_url = os.environ.get(
            "SUCCESS_URL", "http://localhost:8000/payment/success/"
        )
        cancel_url = os.environ.get(
            "CANCEL_URL", "http://localhost:8000/payment/cancel/"
        )

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Borrowing: {borrowing.book.title}",
                        },
                        "unit_amount": int(
                            borrowing.calculate_total_price() * 100
                        ),  # в центах
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {"id": session.id, "url": session.url}

    @csrf_exempt
    def stripe_webhook(request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Обробка події успішної оплати
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            session_id = session.get("id")

            # Знаходимо відповідну оплату
            payment = Payment.objects.filter(session_id=session_id).first()
            if payment:
                # Оновлюємо статус оплати
                payment.status = "PAID"
                payment.save()

                # Відправка повідомлення в Telegram
                borrowing = Borrowing.objects.get(payment=payment)
                send_telegram_message(
                    f"Оплата за книгу '{borrowing.book.title}' успішна! Дякуємо!"
                )

        return JsonResponse({"status": "success"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data["payment_url"] = self.payment_url
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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
