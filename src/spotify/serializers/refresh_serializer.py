from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    refresh_token = serializers.CharField(required=True)
