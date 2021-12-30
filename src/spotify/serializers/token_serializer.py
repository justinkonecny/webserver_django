from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    code = serializers.CharField(required=True)
