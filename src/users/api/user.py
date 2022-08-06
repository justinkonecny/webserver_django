from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.serializers.user import UserResponseSerializer

LOGGER = get_logger(__name__)


class UserViewSet(ViewSet):

    @classmethod
    def list(cls, request: Request) -> Response:
        LOGGER.debug("Handling user request...")

        # serialize the response
        response = UserResponseSerializer(request.user)
        return Response(response.data)
