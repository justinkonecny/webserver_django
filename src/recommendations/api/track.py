from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core import serializers

from logger.logger import get_logger
from recommendations.models import TrackRecommendation
from recommendations.serializers.track import TrackRecommendationToSerializer, TrackRecommendationFromSerializer, UpdateRequestSerializer

LOGGER = get_logger(__name__)


class TrackRecommendationViewSet(ViewSet):
    @classmethod
    def create(cls, request: Request) -> Response:
        LOGGER.debug("Creating track recommendation...")

        # validate the request
        serializer = TrackRecommendationToSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curr_user = request.user
        target_username = serializer.data.get("target_username")
        spotify_track_id = serializer.data.get("spotify_track_id")

        try:
            target_user = User.objects.get(username=target_username)
        except ObjectDoesNotExist:
            return Response("user does not exist", status=status.HTTP_400_BAD_REQUEST)

        TrackRecommendation.objects.create(
            user_from=curr_user,
            user_to=target_user,
            spotify_track_id=spotify_track_id,
        )

        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def list(cls, request: Request) -> Response:
        LOGGER.debug("Getting track recommendation...")

        curr_user = request.user
        tracks = [
            {
                "created_at": track_rec.created_at,
                "from_username": track_rec.user_from.username,
                "spotify_track_id": track_rec.spotify_track_id,
            }
            for track_rec in curr_user.track_recommendation_to.filter(has_listened=False).order_by("created_at").all()
        ]

        # serialize the response
        response = TrackRecommendationFromSerializer(tracks, many=True)
        return Response(response.data)

    @classmethod
    def put(cls, request: Request) -> Response:
        LOGGER.debug("Updating track recommendation...")

        # validate the request
        serializer = UpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curr_user = request.user
        from_username = serializer.data.get("from_username")
        spotify_track_id = serializer.data.get("spotify_track_id")

        try:
            # try to find the user with the given username
            from_user = User.objects.get(username=from_username)
        except ObjectDoesNotExist:
            LOGGER.debug("User not found")
            return Response("user does not exist", status=status.HTTP_400_BAD_REQUEST)

        try:
            # try to find the track recommendation
            track = curr_user.track_recommendation_to.filter(
                user_from=from_user,
                spotify_track_id=spotify_track_id,
                has_listened=False
            ).earliest("created_at")
        except ObjectDoesNotExist:
            LOGGER.debug(f"Recommendation not found: user_from={from_user}, uri={spotify_track_id}")
            return Response("recommendation does not exist", status=status.HTTP_400_BAD_REQUEST)

        # mark the track as listened
        track.has_listened = True
        track.save()

        return Response(status=status.HTTP_200_OK)
