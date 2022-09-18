from collections import defaultdict

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from logger.logger import get_logger
from recommendations.serializers.track import TrackRecommendationSerializer
from recommendations.utils import get_tracks_from_query

LOGGER = get_logger(__name__)


class HistoryRecommendationViewSet(ViewSet):
    @classmethod
    @action(methods=['get'], url_path='to-me', detail=False)
    def get_history_to_me(cls, request: Request) -> Response:
        LOGGER.debug("Getting recommendation history to me...")

        curr_user = request.user
        results = curr_user \
            .track_recommendation_to \
            .filter(has_listened=True) \
            .order_by("-created_at") \
            .all()

        unique_tracks = get_tracks_from_query(results)

        # serialize the response
        response = TrackRecommendationSerializer(unique_tracks, many=True)
        return Response(response.data)

    @classmethod
    @action(methods=['get'], url_path='from-me', detail=False)
    def get_history_from_me(cls, request: Request) -> Response:
        LOGGER.debug("Getting recommendation history from me...")

        curr_user = request.user
        results = curr_user \
            .track_recommendation_from \
            .order_by("-created_at") \
            .all()

        unique_tracks = get_tracks_from_query(results)

        # serialize the response
        response = TrackRecommendationSerializer(unique_tracks, many=True)
        return Response(response.data)
