from rest_framework import serializers


class TrackRecommendationSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    created_at = serializers.DateTimeField(required=True)
    from_username = serializers.CharField(required=True)
    to_username = serializers.CharField(required=True)
    has_listened = serializers.BooleanField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)


class UpdateRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    from_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)
