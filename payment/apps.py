from django.apps import AppConfig


def ready(self):
    import payment.signals


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment"
