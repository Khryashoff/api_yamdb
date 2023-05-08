from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly

from .serializers import (
    TitleSerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
    CategorySerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    """Набор представлений для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """Набор представлений для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Набор представлений для работы с произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Набор представлений для работы с отзывами."""
#     POST работает при обязательном указании title и author (не как в ТЗ)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (AuthorOrReadOnly,)

    # def get_serializer_class(self):
    #     # если запрашивается review_id
    #     if self.action == 'retrieve':
    #         return ReviewRetrySerializer

    #     return ReviewSerializer


    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user, title=get_object_or_404(Title, pk=self.kwargs.get("title_id")))


class CommentViewSet(viewsets.ModelViewSet):
    """Набор представлений для работы с комментариями."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
