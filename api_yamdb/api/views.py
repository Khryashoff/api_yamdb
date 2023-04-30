from django.shortcuts import get_object_or_404
from django.db.models import Avg
from reviews.models import Title, Review, Comment
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly

from .serializers import (
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    # pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        pk = self.kwargs.get("review_id")
        if not pk:
                # тут необходимо ограничить вывод по title_id
                # подумать после доработки моделей:
                #    title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
                #     return title.reviews 
            return Review.objects.all() 
        queryset = get_object_or_404(Review, pk=pk)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

