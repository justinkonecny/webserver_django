from rest_framework import routers

from groups.api import GroupViewSet

router = routers.SimpleRouter()

router.register('', GroupViewSet, basename='')

urlpatterns = router.urls
