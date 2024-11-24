from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view

from books.models import Book
from books.serializers import BookSerializer, BookDetailSerializer, BookListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission class:
    - Allows read-only access to all users.
    - Allows write access only to admin users.
    """

    def has_permission(self, request, view):
        if view.action in ["create", "update", "partial_update", "destroy"]:
            return request.user and request.user.is_staff
        return True


@extend_schema_view(
    list=extend_schema(
        summary="List all books",
        description="Retrieve a list of all books with minimal details.",
        responses={200: BookListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve book details",
        description="Retrieve detailed information about a specific book.",
        responses={200: BookDetailSerializer},
    ),
    create=extend_schema(
        summary="Create a new book",
        description="Create a new book entry. Only accessible to admin users.",
        request=BookSerializer,
        responses={201: BookSerializer},
    ),
    update=extend_schema(
        summary="Update a book",
        description="Update an existing book. Only accessible to admin users.",
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Update specific fields of a book. Only accessible to admin users.",
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Delete a book. Only accessible to admin users.",
        responses={204: None},
    ),
)
class BookListView(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    - Read-only access for all users.
    - Create, update, and delete access for admin users only.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    action_serializer_classes = {
        "list": BookListSerializer,
        "retrieve": BookDetailSerializer,
    }

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        return self.action_serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self):
        """
        Return the queryset for the books.
        - All books are available for viewing.
        """
        return super().get_queryset()
