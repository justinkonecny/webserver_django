from typing import Optional

from rest_framework import serializers

from groups.models import Group
from users.serializers.user import UserResponseSerializer, PublicUserResponseSerializer, UsernameUserResponseSerializer


class CreateGroupRequest(serializers.Serializer):
    passcode = serializers.CharField(required=False, max_length=16)

    def create(self, validated_data) -> Group:
        user = self.context['request'].user
        return Group.objects.create(
            is_active=True,
            passcode=validated_data.get('passcode') or "",
            creator=user
        )

    @staticmethod
    def validate_passcode(value: str) -> str:
        if len(value) > 0 and not value.isalnum():
            raise serializers.ValidationError("invalid passcode: must be alphanumeric")
        return value


class GroupTrackResponseSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    queued_by_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, max_length=128)
    listened = serializers.CharField(required=True)


class QueueGroupTrackRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    group_join_key = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, max_length=128)


class SetListenedGroupTrackRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    group_join_key = serializers.CharField(required=True)
    queued_by_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, max_length=128)


class DeactivateGroupRequest(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    group_join_key = serializers.CharField(required=True)


class GroupResponseSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    join_key = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)
    passcode = serializers.CharField(required=True)
    creator = PublicUserResponseSerializer(required=True, many=False)
    leaders = PublicUserResponseSerializer(required=True, many=True)
    members = PublicUserResponseSerializer(required=True, many=True)
    tracks = GroupTrackResponseSerializer(required=True, many=True)


class JoinGroupRequest(serializers.Serializer):
    join_key = serializers.CharField(required=True)
    passcode = serializers.CharField(required=False, max_length=16)
