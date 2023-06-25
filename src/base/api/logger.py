from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from webserver import settings
from django.urls import get_resolver

LOGGER = get_logger(__name__)


class LoggerViewSet(ViewSet):
    permission_classes = [AllowAny]

    @classmethod
    @csrf_exempt
    @action(methods=['post'], url_path='log', detail=False)
    def create_log(cls, request: Request) -> Response:
        if not settings.DEBUG:
            return Response(status=status.HTTP_403_FORBIDDEN)

        class_name = request.data['class']
        message = request.data['message']
        prefix = "[CLIENT]" if request.user is None else f"[CLIENT][{request.user.username}]"
        LOGGER.info(f"{prefix}[{class_name}]: {message}")
        return Response(status=status.HTTP_200_OK)

    @classmethod
    @action(methods=['get'], url_path='urls', detail=False)
    def get_urls(cls, request: Request) -> Response:
        LOGGER.debug("Getting all endpoints...")
        values = get_resolver().reverse_dict.values()
        for endpoint in values:
            LOGGER.debug(f"[ENDPOINT]: {str(endpoint)}")
        return Response(status=status.HTTP_200_OK)
