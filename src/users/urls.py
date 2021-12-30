from rest_framework import routers

from users.api.login_view_set import LoginViewSet
from users.api.signup_view_set import SignupViewSet

router = routers.SimpleRouter()

router.register('signup', SignupViewSet, basename='users')
router.register('login', LoginViewSet, basename='users')

urlpatterns = router.urls
