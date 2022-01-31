from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.serializers.signup_serializer import SignupRequestSerializer
from users.serializers.user_serializer import UserResponseSerializer

LOGGER = get_logger(__name__)


class SignupViewSet(ViewSet):
    permission_classes = [AllowAny]

    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling signup request...")

        # validate the request
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # retrieve the request fields
        email = serializer.data.get("email").strip()
        username = serializer.data.get("username").strip()
        first_name = serializer.data.get("first_name").strip()
        last_name = serializer.data.get("last_name").strip()
        password = serializer.data.get("password")

        # create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # serialize the response
        response = UserResponseSerializer(user)
        return Response(response.data)
