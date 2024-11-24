from django.urls import path, include
from rest_framework import routers

from books.views import BookListView

app_name = "books"

router = routers.DefaultRouter()
router.register("books", BookListView, basename="books")
urlpatterns = [path("", include(router.urls))]
