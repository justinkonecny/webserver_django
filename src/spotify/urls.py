from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('token', views.SpotifyTokenViewSet, basename='spotify')
router.register('refresh_token', views.SpotifyRefreshViewSet, basename='spotify')

urlpatterns = router.urls
