from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('token', views.SpotifyTokenViewSet, basename='spotify')

urlpatterns = router.urls
