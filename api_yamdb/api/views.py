from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly

from .serializers import (
    TitleListSerializer,
    TitleDetailSerializer,
    GenreSerializer,
    ReviewSerializer,
    #ReviewCreateListSerializer,
    CommentSerializer,
    CategorySerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    list_serializer_class = TitleListSerializer
    detail_serializer_class = TitleDetailSerializer 
    pagination_class = LimitOffsetPagination
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.detail_serializer_class
    

class ReviewViewSet(viewsets.ModelViewSet):
#     POST работает при обязательном указании title и author (не как в ТЗ)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset
    
    # def get_serializer_class(self):
    #     # if self.action == 'retrieve':
    #     #     return ReviewCreateListSerializer
    #     return ReviewSerializer 

    def perform_create(self, serializer_class):
        serializer_class.save(author=1, title=get_object_or_404(Title, pk=self.kwargs.get("title_id"))) #self.request.user


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments

    # def perform_create(self, serializer):
    #     review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
    #     serializer.save(author=self.request.user, review=review)

