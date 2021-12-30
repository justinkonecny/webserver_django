from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
