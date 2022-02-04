from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from users.models import UserFriend
from users.serializers.friend_serializer import FriendRequestSerializer, FriendResponseSerializer

LOGGER = get_logger(__name__)


class FriendViewSet(ViewSet):

    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Handling friend request...")

        # validate the request
        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # retrieve the request fields
        username = serializer.data.get("username").strip()

        try:
            target_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response("user does not exist", status=status.HTTP_400_BAD_REQUEST)

        # query for this user's friends
        curr_user = request.user
        friends = curr_user.get_friends()

        # return error if they're already friends
        if target_user in friends:
            return Response("users already friends", status=status.HTTP_400_BAD_REQUEST)

        # save the friend to the database
        UserFriend.objects.create(
            user_from=request.user,
            user_to=target_user
        )

        # serialize the response
        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def list(cls, request: Request) -> Response:
        LOGGER.debug("Handling friend query...")

        # query for all friends of this user
        curr_user = request.user
        friends = curr_user.get_friends()

        # serialize the response
        response = FriendResponseSerializer(friends, many=True)
        return Response(response.data)
