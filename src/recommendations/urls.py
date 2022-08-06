from rest_framework import routers

from recommendations.api.track import TrackRecommendationViewSet

router = routers.SimpleRouter()

router.register('tracks', TrackRecommendationViewSet, basename='recommendations')

urlpatterns = router.urls
