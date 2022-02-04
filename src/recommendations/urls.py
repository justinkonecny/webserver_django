from rest_framework import routers

from recommendations.api.track_recommendation_view_set import TrackRecommendationViewSet

router = routers.SimpleRouter()

router.register('tracks', TrackRecommendationViewSet, basename='recommendations')

urlpatterns = router.urls
