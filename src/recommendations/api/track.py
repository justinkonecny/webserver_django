from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from recommendations.models import TrackRecommendation
from recommendations.serializers.track import TrackRecommendationToSerializer, TrackRecommendationFromSerializer

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
            for track_rec in curr_user.track_recommendation_to.all().order_by("created_at")
        ]

        # serialize the response
        response = TrackRecommendationFromSerializer(tracks, many=True)
        return Response(response.data)

    @classmethod
    def update(cls, request: Request) -> Response:
        LOGGER.debug("Updating track recommendation...")

        return Response(status=status.HTTP_200_OK)
