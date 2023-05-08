from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg("score"))
        return obj["rating"]


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для записи."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if 1 >= value >= 10:
            raise serializers.ValidationError('Значения score от 1 до 10!')
        return value

    def validate(self, attrs): #дополнить
        author = attrs.get('author')
        title = attrs.get('title')
        if Review.objects.filter(
            author=author, title=title
        ).exists():
            raise serializers.ValidationError(
                'Допускается только один отзыв!')
        return attrs


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
