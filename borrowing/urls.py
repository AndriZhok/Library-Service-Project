from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowingViewSet

app_name = "borrowings"

router = DefaultRouter()
router.register(r"", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path("", include(router.urls)),
    path("webhook/", BorrowingViewSet.stripe_webhook, name="stripe-webhook"),
]
