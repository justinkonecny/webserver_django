from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.serializers.login_serializer import LoginRequestSerializer
from users.serializers.user_serializer import UserResponseSerializer

LOGGER = get_logger(__name__)


class LoginViewSet(ViewSet):
    permission_classes = [AllowAny]

    @classmethod
    @csrf_exempt
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling login request...")

        # validate the request
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # retrieve the request fields
        username = serializer.data.get("username").strip()
        password = serializer.data.get("password")

        # authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            return Response("invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

        # log the user in
        login(request=request, user=user)

        # serialize the response
        response = UserResponseSerializer(user)
        return Response(response.data)
