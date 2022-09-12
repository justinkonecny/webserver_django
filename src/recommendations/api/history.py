from functools import reduce

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


class HistoryRecommendationViewSet(ViewSet):

    @classmethod
    def list(cls, request: Request) -> Response:
        LOGGER.debug("Getting recommendation history...")

        curr_user = request.user
        tracks = [
            {
                "created_at": track_rec.created_at,
                "from_username": track_rec.user_from.username,
                "spotify_track_id": track_rec.spotify_track_id,
            }
            for track_rec in curr_user.track_recommendation_to.filter(has_listened=True).order_by("-created_at").all()
        ]

        unique = tracks[:1]
        for track in tracks[1:]:
            last_track = unique[-1]
            if track["spotify_track_id"] != last_track["spotify_track_id"]:
                unique.append(track)

        # serialize the response
        response = TrackRecommendationFromSerializer(unique, many=True)
        return Response(response.data)
