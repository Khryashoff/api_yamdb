from django.db.models import Avg
from rest_framework import serializers
from api_yamdb.settings import EMAIL, USERNAME_NAME

from users.models import User
from users.validators import ValidateUsername

from reviews.models import Category, Genre, Title, Review, Comment


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Users.
    """
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class RegistrationSerializer(serializers.Serializer, ValidateUsername):
    """
    Сериализатор для проверки и сохранения данных при регистрации пользователя.
    """
    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    email = serializers.EmailField(required=True, max_length=EMAIL)


class TokenSerializer(serializers.Serializer, ValidateUsername):
    """
    Сериализатор для проверки и авторизации пользователя.
    """
    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(UsersSerializer):
    """
    Сериализатор модели User для методов GET и PATCH.
    """
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category.
    """
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Genre.
    """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title для получения информации о произведении.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
            'rating',
        )

    def get_rating(self, obj):
        """
        Возвращает среднюю оценку для объекта Title.
        """
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title для добавления новых произведений.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения отзыва по id.
    """
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'pub_date',
            'text',
            'score',
        )

    def validate_score(self, value):
        """
        Производит валидацию поля score на
        соответствие установленному диапазону.
        """
        if 1 >= value >= 10:
            raise serializers.ValidationError('Значения score от 1 до 10!')
        return value

    def validate(self, attrs):
        """
        Производит валидацию допустимости создания нового отзыва.
        """
        author = attrs.get('author')
        title = attrs.get('title')
        if Review.objects.filter(
            author=author, title=title
        ).exists():
            raise serializers.ValidationError(
                'Допускается только один отзыв!')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = '__all__'
