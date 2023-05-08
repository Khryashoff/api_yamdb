from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import AuthorAdminModerator
from .serializers import (
    TitleRetrieveSerializer,
    TitleCreateSerializer,
    GenreSerializer,
    ReviewSerializer,
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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.read_serializer_class
        return self.create_serializer_class

    def get_permission_class(self):
        if self.action in ['list', 'retrieve']:
            return AllowAny
        return IsAdminUser


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset

    def get_permission_class(self):
        if self.action == 'list':
            return AllowAny
        if self.action in ['create', 'retrieve']:
            return IsAuthenticated
        if self.action in ['patch', 'delete']:
            return AuthorAdminModerator

    def perform_create(self, serializer_class):
        try:
            title = get_object_or_404(
                Title,
                pk=self.kwargs.get('title_id')
            )
            serializer_class.save(author=self.request.user, title=title)
        except: pass #вместо try/except провалидировать повторный отзыв на то же произведение?


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)

    def get_permission_class(self):
        if self.action in ['list', 'retrieve']:
            return AllowAny
        if self.action == 'create':
            return IsAuthenticated
        if self.action in ['patch', 'delete']:
            AuthorAdminModerator
