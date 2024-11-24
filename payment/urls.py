from rest_framework.routers import DefaultRouter
from payment.views import PaymentViewSet, payment_success, payment_cancel
from django.urls import path, include

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("success/", payment_success, name="payment-success"),
    path("cancel/", payment_cancel, name="payment-cancel"),
]
