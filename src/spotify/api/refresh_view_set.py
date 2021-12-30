from rest_framework.request import Request
from rest_framework.response import Response

from logger.logger import get_logger
from spotify.serializers.refresh_serializer import RefreshSerializer
from spotify.views import SpotifyView

LOGGER = get_logger(__name__)


class RefreshViewSet(SpotifyView):
    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling refresh token request...")

        # validate the request
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.data.get("refresh_token")

        try:
            # attempt to make the request to spotify
            token = cls.request_refresh_token(refresh_token)
            return Response(token)
        except ValueError as e:
            return Response(str(e))

    @classmethod
    def request_refresh_token(cls, refresh_token: str) -> str:
        # construct the endpoint
        form = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        # make request to spotify
        return cls._make_authorized_request(form)
