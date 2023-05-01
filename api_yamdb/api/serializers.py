from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User.
    """
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category.
    """
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
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

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg("score"))
        return obj["rating"]


class ReviewSerializer(serializers.ModelSerializer):
    # title = serializers.SlugRelatedField(
    #     slug_field='id', # choices: category, category_id, description, genre, id, name, reviews, year
    #     many=True,
    #     queryset=Title.objects.all()
    # )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Review
        fields = ("id", "title", "text", "score", "author", "pub_date")

    # дописать def create(self, validated_data):


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
