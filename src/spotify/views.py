import base64
import json
from abc import ABC
from json import JSONDecodeError

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger

LOGGER = get_logger(__name__)


class SpotifyView(ABC, ViewSet):
    @staticmethod
    def _get_auth_header() -> dict[str, str]:
        LOGGER.debug("Constructing authentication header...")

        # read the configurable settings / secrets
        client_id = getattr(settings, "SPOTIFY_CLIENT_ID")
        client_secret = getattr(settings, "SPOTIFY_CLIENT_SECRET")

        # construct the auth header
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        return {"Authorization": f"Basic {auth_header}"}

    @classmethod
    def _make_authorized_request(cls, form: dict) -> str:
        LOGGER.debug("Making authorized request to Spotify...")

        spotify_endpoint = getattr(settings, "SPOTIFY_ACCOUNTS_ENDPOINT")

        # make the request to spotify
        response = requests.post(
            spotify_endpoint,
            data=form,
            headers=cls._get_auth_header()
        )

        # parse the response
        content = response.content.decode()
        status_code = response.status_code

        if status_code != status.HTTP_200_OK:
            err_msg = cls._get_error_message(content, status_code)
            raise ValueError(err_msg)

        return content

    @classmethod
    def _get_error_message(cls, content: str, status_code: int) -> str:
        LOGGER.debug("Parsing error message...")

        err_msg = f"Received invalid HTTP response ({status_code})"
        try:
            data = json.loads(content)
            if "error" in data:
                err_msg += f" with error: {data['error']}"
        except JSONDecodeError:
            pass
        return err_msg
