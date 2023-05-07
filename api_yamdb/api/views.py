from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from .permissions import AuthorOrReadOnly

from .serializers import (
    TitleRetrieveSerializer,
    TitleCreateSerializer,
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
    read_serializer_class = TitleRetrieveSerializer
    create_serializer_class = TitleCreateSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == ('list' or 'retrive'):
            return self.read_serializer_class
        return self.create_serializer_class


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))

    def get_queryset(self):
        # title = get_object_or_404(, pk=self.kwargs.get("title_id"))
        # queryset = title.reviews.all()
        queryset = Title.objects.all().annotate(
            rating=Avg('reviews__score')
        )
        return queryset
    
    # def get_serializer_class(self):
    #     # if self.action == 'retrieve':
    #     #     return ReviewCreateListSerializer
    #     return ReviewSerializer 

    def perform_create(self, serializer_class):
        serializer_class.save(
            author=self.request.user,
            title=get_object_or_404(
                Title,
                pk=self.kwargs.get("title_id")
            )  
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments

    # def perform_create(self, serializer):
    #     review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
    #     serializer.save(author=self.request.user, review=review)

