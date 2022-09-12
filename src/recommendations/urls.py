from rest_framework import routers

from recommendations.api.history import HistoryRecommendationViewSet
from recommendations.api.track import TrackRecommendationViewSet

router = routers.SimpleRouter()

router.register('tracks', TrackRecommendationViewSet, basename='recommendations')
router.register('history', HistoryRecommendationViewSet, basename='recommendations')

urlpatterns = router.urls
