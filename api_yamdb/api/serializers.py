from django.shortcuts import get_object_or_404
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
    """Сериализатор модели Category."""
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = '__all__'


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для представления списка."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
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


#поменять
class TitleDetailSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для объекта."""

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
    """Сериализатор для получения отзыва."""
    author = 1
    # author = serializers.SlugRelatedField(
    #     default=serializers.CurrentUserDefault(),
    #     required=False,
    #     slug_field='author',
    #     queryset=User.objects.all(),
    # )
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

# class ReviewCreateListSerializer(serializers.ModelSerializer):
#     """Сериализатор для получения списка и создания отзыва."""
#     def validate(self, data):
#         request = self.context.get('request')

#         if request.method == 'POST':
#             title_id = self.context['view'].kwargs.get('title_id')
#             title = get_object_or_404(Title, pk=title_id)
#             if Review.objects.filter(
#                     author=request.user, title=title
#             ).exists():
#                 raise serializers.ValidationError(
#                     'Допускается только один отзыв!')
#         return data

#     class Meta:
#         model = Review
#         fields = (
#             "title",
#             "author",
#             "text",
#             "score")

    # дописать def create(self, validated_data):


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
