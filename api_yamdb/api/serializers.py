from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = '__all__'


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer()
    category = CategorySerializer()   
    rating = serializers.SerializerMethodField(read_only=True)

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

    # def get_rating(self, obj):
    #     obj = obj.reviews.all().aggregate(rating=Avg("score"))
    #     return obj["rating"]


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для записи."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = CategorySerializer()

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
    """Сериализатор для получения отзыва."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        required=False,
        slug_field='author',
        queryset=User.objects.all(),
    )
    title = serializers.SlugRelatedField(
        required=False,
        queryset=Title.objects.all(),
        slug_field='title'
    ) #объект title в url
    

    class Meta:
        model = Review
        fields = (
            "title",
            "author",
            "text",
            "score")

    def validate(self, attrs):
        author = attrs.get('author')
        title = attrs.get('title')
        if Review.objects.filter(
            author=author, title=title
        ).exists():
            raise serializers.ValidationError(
                'Допускается только один отзыв!')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
