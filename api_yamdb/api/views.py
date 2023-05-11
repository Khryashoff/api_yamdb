from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from reviews.models import Genre, Category, Title, Review, Comment

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminOnly,
                          IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)

from .serializers import (UsersSerializer,
                          UserEditSerializer,
                          RegistrationSerializer,
                          TokenSerializer)

from .serializers import (TitleRetrieveSerializer,
                          TitleCreateSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          CategorySerializer)


@api_view(['POST'])
def register_user(request):
    """
    Осуществляет регистрацию новых пользователей.
    Генерирует и отправляет код подтверждения на почту.
    """
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError(
            'username или email заняты!', status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """
    Получает токен доступа для пользователя с указанными
    username и confirmation_code.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для работы с User.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    @action(
        methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def get_edit_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Набор представлений для работы с Genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Набор представлений для работы с Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для работы с Title.
    """
    queryset = Title.objects.all()
    read_serializer_class = TitleRetrieveSerializer
    create_serializer_class = TitleCreateSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.read_serializer_class
        return self.create_serializer_class


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для работы с Review.
    """
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer_class):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer_class.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для работы с Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

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
