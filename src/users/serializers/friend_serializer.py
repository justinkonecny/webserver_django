from rest_framework import serializers


class FriendRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    username = serializers.CharField(required=True)


class FriendResponseSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
