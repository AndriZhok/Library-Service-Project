from rest_framework import viewsets

from books.models import Book
from books.serializers import BookSerializer, BookDetailSerializer, BookListSerializer


class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    action_serializer_classes = {
        "list": BookListSerializer,
        "retrieve": BookDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self):
        return super().get_queryset()
