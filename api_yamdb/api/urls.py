from api.views import TitleViewSet, ReviewViewSet, CommentViewSet
from django.urls import include, path
from rest_framework import routers


router_v1 = routers.DefaultRouter()
router_v1.register(r"titles", TitleViewSet)
router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet,
                   basename="reviews")
router_v1.register(r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)comments",
                   CommentViewSet,
                   basename="comments")

urlpatterns = [
    path("v1/", include((router_v1.urls, 'api'), namespace="v_1")),
]
