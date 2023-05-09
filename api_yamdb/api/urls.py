from api.views import (TitleViewSet, ReviewViewSet, CommentViewSet,
                       GenreViewSet, CategoryViewSet)
from django.views.generic import TemplateView
from .views import (UserViewSet, get_token, register_user)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from users.views import UsersViewSet


router_v1 = DefaultRouter()
# router_v1.register(r"users/me", UsersViewSet)
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r"genres", GenreViewSet)
router_v1.register(r"categories", CategoryViewSet)
router_v1.register(r"titles", TitleViewSet)
router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet,
                   basename="reviews")
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments',
                   CommentViewSet,
                   basename="comments")

urlpatterns_auth = [
    path('signup/', register_user, name='register_user'),
    path('token/', get_token, name='token'),
]


urlpatterns = [
    path("v1/", include((router_v1.urls, 'api'), namespace="v_1")),
    path('v1/auth/', include(urlpatterns_auth)),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
