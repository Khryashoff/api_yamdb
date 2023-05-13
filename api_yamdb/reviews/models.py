from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User

from api_yamdb.settings import (NAME_LENGTH, DESCRIPTION_LENGTH,
                                FIRST_CHARACTERS_OF_TEXT,
                                MAX_RATING, MIN_RATING)
from reviews.validators import validate_year_not_future
from reviews.base import CategoryGenreModel


class Category(CategoryGenreModel):
    """
    Класс, представляющий категории.
    """
    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    """
    Класс, представляющий жанры.
    """
    class Meta:
        ordering = ['id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Класс, представляющий произведение.
    """
    category = models.ForeignKey(
        Category,
        verbose_name='Категория контента',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр контента',
        related_name='titles',
    )
    name = models.CharField(
        verbose_name='Наименование произведения',
        max_length=NAME_LENGTH,
    )
    year = models.IntegerField(
        verbose_name='Дата релиза произведения',
        validators=[validate_year_not_future],
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        default='Нет описания',
        max_length=DESCRIPTION_LENGTH,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return f'{self.name} {self.genres}'


class Review(models.Model):
    """
    Класс, представляющий отзывы.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
    )
    text = models.TextField(
        max_length=DESCRIPTION_LENGTH,
        blank=False
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)
        ],
        blank=False,
        default=MIN_RATING
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self) -> str:
        return self.text[:FIRST_CHARACTERS_OF_TEXT]


class Comment(models.Model):
    """
    Класс, представляющий комментарии.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
    )
    text = models.TextField(
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.text[:FIRST_CHARACTERS_OF_TEXT]
