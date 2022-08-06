from rest_framework import serializers


class UserResponseSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
