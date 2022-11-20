from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.serializers.signup import SignupRequestSerializer
from users.serializers.user import UserResponseSerializer

LOGGER = get_logger(__name__)


class SignupViewSet(ViewSet):
    permission_classes = [AllowAny]

    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling signup request...")

        # validate the request
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create the user
        user = serializer.save()

        # serialize the response
        response = UserResponseSerializer(user)
        return Response(response.data)
