from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet, get_token,
                    register_user)

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns_auth = [
    path('signup/', register_user, name='register_user'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]