from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.serializers.search import SearchRequestSerializer, SearchResponseSerializer

LOGGER = get_logger(__name__)


class SearchViewSet(ViewSet):

    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling search query...")

        # validate the request
        serializer = SearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # retrieve the request fields
        username = serializer.data.get("username").strip()

        target_users = User.objects.filter(username__icontains=username).exclude(username=request.user.username)

        # serialize the response
        response = SearchResponseSerializer(target_users, many=True)
        return Response(response.data)
