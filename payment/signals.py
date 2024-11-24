from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowing.models import Borrowing
from models import Payment
from stripe_service import create_payment_session
from django.conf import settings


@receiver(post_save, sender=Borrowing)
def create_payment_for_borrowing(sender, instance, created, **kwargs):
    if created:
        total_price = instance.book.daily_fee * instance.expected_return_date.day

        session = create_payment_session(
            amount=float(total_price),
            currency="usd",
            success_url=f"{settings.FRONTEND_URL}/success/",
            cancel_url=f"{settings.FRONTEND_URL}/cancel/",
        )

        Payment.objects.create(
            borrowing=instance,
            money_to_pay=total_price,
            session_url=session.url,
            session_id=session.id,
        )
