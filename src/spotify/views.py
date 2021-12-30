import base64
import json
from abc import ABC
from json import JSONDecodeError

import requests
from django.conf import settings
from django.http.request import QueryDict
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
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


class SpotifyRefreshViewSet(SpotifyView):
    @classmethod
    def create(cls, request: Request) -> HttpResponse:
        LOGGER.debug("Handling refresh token request...")

        data: QueryDict = request.data
        refresh_token = data.get("refresh_token", None)

        # validate the request
        if refresh_token is None or type(refresh_token) != str:
            return Response("missing or invalid form data 'refresh_token'", status.HTTP_400_BAD_REQUEST)

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


class SpotifyTokenViewSet(SpotifyView):
    @classmethod
    def create(cls, request: Request) -> HttpResponse:
        LOGGER.debug("Handling auth token request...")

        data: QueryDict = request.data
        code = data.get("code", None)

        # validate the request
        if code is None or type(code) != str:
            return Response("missing or invalid form data 'code'", status.HTTP_400_BAD_REQUEST)

        try:
            # attempt to make the request to spotify
            token = cls.request_auth_token(code)
            return Response(token)
        except ValueError as e:
            return Response(str(e))

    @classmethod
    def request_auth_token(cls, code: str) -> str:
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
