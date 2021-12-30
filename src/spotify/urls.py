from rest_framework import routers

from spotify.api.refresh_view_set import RefreshViewSet
from spotify.api.token_view_set import TokenViewSet

router = routers.SimpleRouter()

router.register('token', TokenViewSet, basename='spotify')
router.register('refresh', RefreshViewSet, basename='spotify')

urlpatterns = router.urls
