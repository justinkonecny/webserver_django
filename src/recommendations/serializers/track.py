from rest_framework import serializers


class TrackRecommendationSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    created_at = serializers.DateTimeField(required=True)
    from_username = serializers.CharField(required=True)
    to_username = serializers.CharField(required=True)
    has_listened = serializers.BooleanField(required=True)
    rating = serializers.IntegerField(required=True, allow_null=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)


class NewTrackRecommendationSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    target_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)


class UpdateRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    from_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)


class UpdateRatingRequestSerializer(serializers.Serializer):
    # don't define the `create(...)` or `update(...)` methods
    from_username = serializers.CharField(required=True)
    spotify_track_id = serializers.CharField(required=True, min_length=6)
    rating = serializers.IntegerField(required=True, min_value=0, max_value=5)
