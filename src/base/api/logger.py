import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger

LOGGER = get_logger(__name__)


class LoggerViewSet(ViewSet):
    @classmethod
    @action(methods=['post'], url_path='log', detail=False)
    def create_log(cls, request: Request) -> Response:
        if request.user.is_staff:
            class_name = request.data['class']
            message = request.data['message']
            LOGGER.info(f"[CLIENT:'{request.user.username}'][{class_name}]: {message}")
        return Response(status=status.HTTP_200_OK)
