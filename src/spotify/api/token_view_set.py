from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response

from logger.logger import get_logger
from spotify.serializers.token_serializer import TokenSerializer
from spotify.views import SpotifyView

LOGGER = get_logger(__name__)


class TokenViewSet(SpotifyView):
    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling auth token request...")

        # validate the request
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data.get("code")

        try:
            # attempt to make the request to spotify
            token = cls.request_auth_token(code)
            return Response(token)
        except ValueError as e:
            return Response(str(e))

    @classmethod
    def request_auth_token(cls, code: str) -> dict[str, str]:
        # read the configurable settings / secrets
        redirect_uri = getattr(settings, "SPOTIFY_CLIENT_CALLBACK")

        # construct the request form
        form = {
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        }

        # make request to spotify
        return cls._make_authorized_request(form)
