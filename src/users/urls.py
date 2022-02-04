from rest_framework import routers

from users.api.friend_view_set import FriendViewSet
from users.api.login_view_set import LoginViewSet
from users.api.signup_view_set import SignupViewSet
from users.api.user_view_set import UserViewSet

router = routers.SimpleRouter()

router.register('signup', SignupViewSet, basename='users')
router.register('login', LoginViewSet, basename='users')
router.register('friends', FriendViewSet, basename='users')
router.register('me', UserViewSet, basename='users')

urlpatterns = router.urls
