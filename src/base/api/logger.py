import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger

LOGGER = get_logger(__name__)


class LoggerViewSet(ViewSet):
    permission_classes = [AllowAny]

    @classmethod
    @csrf_exempt
    @action(methods=['post'], url_path='log', detail=False)
    def create_log(cls, request: Request) -> Response:
        print(request.user)
        LOGGER.info(f"{str(request.user)}")
        class_name = request.data['class']
        message = request.data['message']
        LOGGER.info(f"[CLIENT][{class_name}]: {message}")

        import re
        regex = re.compile('^HTTP_')
        d= dict((regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_'))
        print(d)

        # if request.user.is_staff:
        #     class_name = request.data['class']
        #     message = request.data['message']
        #     LOGGER.info(f"[CLIENT:'{request.user.username}'][{class_name}]: {message}")
        return Response(status=status.HTTP_200_OK)
