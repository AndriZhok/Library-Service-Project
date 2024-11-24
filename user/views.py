from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create a New User",
        description="Register a new user by providing the necessary details.",
        request=UserSerializer,
        responses={201: UserSerializer},
    ),
)
class CreateUserView(generics.CreateAPIView):
    """
    A view for creating new users.
    """

    serializer_class = UserSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve User Details",
        description="Retrieve the details of the currently authenticated user.",
        responses={200: UserSerializer},
    ),
    put=extend_schema(
        summary="Update User Details",
        description="Update all details of the currently authenticated user.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    patch=extend_schema(
        summary="Partially Update User Details",
        description="Partially update details of the currently authenticated user.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    A view for managing the authenticated user's details.
    """

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieve the currently authenticated user.
        """
        return self.request.user
