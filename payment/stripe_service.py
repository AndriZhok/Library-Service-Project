import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_payment_session(
    amount: float, currency: str, success_url: str, cancel_url: str
):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": "Library Payment"},
                        "unit_amount": int(amount * 100),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")
