from rest_framework import serializers


class TrackRecommendationToSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    target_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)


class TrackRecommendationFromSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    from_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)
