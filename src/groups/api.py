from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from groups.serializer import (
    CreateGroupRequest,
    GroupResponseSerializer,
    JoinGroupRequest,
    QueueGroupTrackRequestSerializer,
    SetListenedGroupTrackRequestSerializer,
    DeactivateGroupRequest,
)
from groups.models import GroupMembership, Group, GroupTrack
from logger.logger import get_logger

LOGGER = get_logger(__name__)


def get_group_data(query_results, group_limit=20, track_limit=50) -> list:
    groups = [
        {
            "join_key": group.join_key,
            "is_active": group.is_active,
            "passcode": group.passcode,
            "creator": group.creator,
            "tracks": [
                {
                    "queued_by_username": t.user.username,
                    "spotify_track_id": t.spotify_track_id,
                    "listened": t.listened,
                }
                for t in group.tracks.all().order_by("listened", "created_at")[
                    :track_limit
                ]
            ],
            "leaders": [
                gm.user
                for gm in GroupMembership.objects.filter(group=group, role="LEA")
            ],
            "members": [
                gm.user
                for gm in GroupMembership.objects.filter(group=group, role="FOL")
            ],
        }
        for group in query_results[:group_limit]
    ]
    return groups


class GroupViewSet(ViewSet):
    @classmethod
    @action(methods=["get"], url_path="created", detail=False)
    def get_created(cls, request: Request) -> Response:
        """
        Get all groups created by the user.
        """
        LOGGER.debug("Getting user groups...")

        # try to find the user's created groups
        created_groups = (
            request.user.created_groups.filter(is_active=True)
            .order_by("-created_at")
            .all()
        )

        data = get_group_data(created_groups)
        response = GroupResponseSerializer(data, many=True)
        return Response(response.data)

    @classmethod
    @action(methods=["get"], url_path="joined", detail=False)
    def get_joined(cls, request: Request) -> Response:
        """
        Get all groups the user has joined.
        """
        LOGGER.debug("Getting user joined groups...")

        # try to find the user's groups
        groups = (
            request.user.groups_member_of.filter(is_active=True)
            .order_by("-created_at")
            .all()
        )

        data = get_group_data(groups)
        response = GroupResponseSerializer(data, many=True)
        return Response(response.data)

    @classmethod
    @action(methods=["get"], url_path="active", detail=False)
    def get_active(cls, request: Request) -> Response:
        """
        Get all groups the user has created or
        that are still active joined.
        """
        LOGGER.debug("Getting user active groups...")

        group_key = request.query_params.get("group_join_key")

        # try to find the user's groups
        groups = (
            request.user.get_active_groups(join_key=group_key)
            if group_key is not None
            else request.user.get_active_groups()
        )

        data = get_group_data(groups)
        response = GroupResponseSerializer(data, many=True)
        return Response(response.data)

    @classmethod
    @action(methods=["post"], url_path="create", detail=False)
    def create_group(cls, request: Request) -> Response:
        LOGGER.debug("Creating new group...")

        # validate the request
        serializer = CreateGroupRequest(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # create the new group
        group = serializer.save()
        data = get_group_data([group])[0]

        # serialize the response
        response = GroupResponseSerializer(data)
        return Response(response.data)

    @classmethod
    @action(methods=["post"], url_path="join", detail=False)
    def join_group(cls, request: Request) -> Response:
        LOGGER.debug("Joining group...")

        # validate the request
        serializer = JoinGroupRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_join_key = serializer.data.get("join_key")
        group_passcode = serializer.data.get("passcode")

        fail_msg = "invalid group or passcode"

        try:
            # try to find the given group
            group = Group.objects.get(join_key=group_join_key)
        except ObjectDoesNotExist:
            LOGGER.debug("Group not found")
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

        # ensure the group is still active
        if not group.is_active:
            LOGGER.debug("Group not active")
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

        # ensure the passcode is correct
        if (
            group.passcode is not None
            and len(group.passcode) > 0
            and group.passcode != group_passcode
        ):
            LOGGER.debug("Invalid passcode")
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

        # creator can't join their own group
        if group.creator == request.user:
            LOGGER.debug("Creator attempting to join their own group")
            return Response(
                "creators cannot join their own groups",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if the user is already in the group
        if group.members.contains(request.user):
            LOGGER.debug("User already in group")
            data = get_group_data([group])[0]
            response = GroupResponseSerializer(data)
            return Response(response.data)

        # otherwise, add the user to the group
        LOGGER.debug("Adding user to group")
        GroupMembership.objects.create(
            user=request.user, group=group, role=GroupMembership.GroupRole.FOLLOWER
        )

        # serialize the response
        data = get_group_data([group])[0]
        response = GroupResponseSerializer(data)
        return Response(response.data)

    @classmethod
    @action(methods=["post"], url_path="queue", detail=False)
    def queue_track(cls, request: Request) -> Response:
        LOGGER.debug("Queuing track...")

        # validate the request
        serializer = QueueGroupTrackRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_join_key = serializer.data.get("group_join_key")
        spotify_track_id = serializer.data.get("spotify_track_id")

        try:
            group = request.user.get_active_group(join_key=group_join_key)
        except ObjectDoesNotExist:
            LOGGER.debug("Group not found")
            return Response("no group found", status=status.HTTP_400_BAD_REQUEST)

        # create the group track queue
        GroupTrack.objects.create(
            group=group, user=request.user, spotify_track_id=spotify_track_id
        )

        # serialize the response
        data = get_group_data([group])[0]
        response = GroupResponseSerializer(data)
        return Response(response.data)

    @classmethod
    @action(methods=["post"], url_path="listened", detail=False)
    def set_listened(cls, request: Request) -> Response:
        LOGGER.debug("Marking track listened...")

        # validate the request
        serializer = SetListenedGroupTrackRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_join_key = serializer.data.get("group_join_key")
        queued_by_username = serializer.data.get("queued_by_username")
        spotify_track_id = serializer.data.get("spotify_track_id")

        try:
            # try to find the given group
            group = request.user.get_active_group(join_key=group_join_key)
        except ObjectDoesNotExist:
            LOGGER.debug("Group not found")
            return Response("no group found", status=status.HTTP_400_BAD_REQUEST)

        try:
            # try to find the given group membership
            if group.creator != request.user:
                membership = GroupMembership.objects.get(group=group, user=request.user)
                if membership.role != GroupMembership.GroupRole.LEADER:
                    LOGGER.debug("User not a leader")
                    return Response(
                        "insufficient permissions", status=status.HTTP_403_FORBIDDEN
                    )
        except ObjectDoesNotExist:
            LOGGER.debug("Membership not found")
            return Response(
                "user not a group member", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            track = GroupTrack.objects.filter(
                group=group,
                user__username=queued_by_username,
                spotify_track_id=spotify_track_id,
            ).first()
        except ObjectDoesNotExist:
            LOGGER.debug("No track found")
            return Response("no track found", status=status.HTTP_400_BAD_REQUEST)

        # set the track as listened
        track.listened = True
        track.save()

        # serialize the response
        data = get_group_data([group])[0]
        response = GroupResponseSerializer(data)
        return Response(response.data)

    @classmethod
    @action(methods=["post"], url_path="deactivate", detail=False)
    def deactivate_group(cls, request: Request) -> Response:
        LOGGER.debug("Deactivating group...")

        # validate the request
        serializer = DeactivateGroupRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_join_key = serializer.data.get("group_join_key")

        try:
            # try to find the given group
            group = request.user.get_active_group(join_key=group_join_key)
        except ObjectDoesNotExist:
            LOGGER.debug("Group not found")
            return Response("no group found", status=status.HTTP_400_BAD_REQUEST)

        # only the creator can deactivate a group
        if group.creator != request.user:
            LOGGER.debug("User not group creator")
            return Response(
                "insufficient permissions", status=status.HTTP_403_FORBIDDEN
            )

        # set the group as not active
        group.is_active = False
        group.save()

        return Response(status=status.HTTP_200_OK)
