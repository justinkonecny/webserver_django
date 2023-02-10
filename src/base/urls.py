from rest_framework import routers

from base.api.logger import LoggerViewSet

router = routers.SimpleRouter()

router.register('logger', LoggerViewSet, basename='logger')

urlpatterns = router.urls
