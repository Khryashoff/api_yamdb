from api.views import TitleViewSet, ReviewViewSet, CommentViewSet, GenreViewSet, CategoryViewSet
from users.views import UsersViewSet
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
# router_v1.register(r"auth/signup", )
# router_v1.register(r"auth/token", )
router_v1.register(r"users/me", UsersViewSet)
router_v1.register(r"genres", GenreViewSet)
router_v1.register(r"categories", CategoryViewSet)
router_v1.register(r"titles", TitleViewSet)
router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet,
                   basename="reviews")
router_v1.register(r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)comments",
                   CommentViewSet,
                   basename="comments")

urlpatterns = [
    path("v1/", include((router_v1.urls, 'api'), namespace="v_1")),
    path("v1/", include((router_v1.urls, 'api_users'), namespace="v1")),
]