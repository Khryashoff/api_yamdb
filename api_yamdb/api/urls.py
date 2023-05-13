from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (UserViewSet, get_token, register_user,
                       GenreViewSet, CategoryViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet)


app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments',
                   CommentViewSet,
                   basename='comments')


urlpatterns_auth = [
    path('signup/', register_user, name='register_user'),
    path('token/', get_token, name='token'),
]


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/', include((router_v1.urls, 'api'), namespace='v_1')),
    path('v1/auth/', include(urlpatterns_auth)),
]
