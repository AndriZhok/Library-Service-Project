from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from books.serializers import BookSerializer, BookDetailSerializer, BookListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create", "update", "partial_update", "destroy"]:
            return request.user and request.user.is_staff
        return True


class BookListView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
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
