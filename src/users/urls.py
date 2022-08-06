from rest_framework import routers

from users.api.friend import FriendViewSet
from users.api.login import LoginViewSet
from users.api.signup import SignupViewSet
from users.api.user import UserViewSet
from users.api.search import SearchViewSet

router = routers.SimpleRouter()

router.register('signup', SignupViewSet, basename='users')
router.register('login', LoginViewSet, basename='users')
router.register('friends', FriendViewSet, basename='users')
router.register('search', SearchViewSet, basename='users')
router.register('me', UserViewSet, basename='users')

urlpatterns = router.urls
