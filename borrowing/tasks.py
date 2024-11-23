import os
import requests

from celery import shared_task
from datetime import date

from dotenv import load_dotenv

from .models import Borrowing

load_dotenv()

TELEGRAM_API_URL = os.environ.get("TELEGRAM_URL")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


@shared_task
def notify_overdue_borrowings():
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=date.today(), actual_return_date__isnull=True
    )
    for borrowing in overdue_borrowings:
        message = (
            f"Книга '{borrowing.book.title}' прострочена. "
            f"Очікувана дата повернення: {borrowing.expected_return_date}."
        )
        data = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(TELEGRAM_API_URL, data=data)
        if response.status_code != 200:
            raise Exception(f"Не вдалося відправити повідомлення: {response.text}")


def send_telegram_message(chat_id, message):
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(TELEGRAM_API_URL, data=data)
    if response.status_code != 200:
        raise Exception(f"Не вдалося відправити повідомлення: {response.text}")
