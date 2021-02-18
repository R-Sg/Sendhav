
from rest_framework import routers

from .views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
# Some Auth API's:-
    # /api/auth/login :- POST
    # /api/auth/register :- POST
    # /api/auth/logout :- POST
    # /api/auth/password_change :- POST
 