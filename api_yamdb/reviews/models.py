from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from api_yamdb.settings import FIRST_CHARACTERS_OF_TEXT

from .validators import validate_year_not_future


class Category(models.Model):
    """Класс, представляющий категории."""
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

    # def __str__(self) -> str:
    #     return f'{self.name}, {self.slug}' # изменить ?{'name': 'Фильм', 'slug': 'films'}


class Genre(models.Model):
    """Класс, представляющий жанры."""
    name = models.CharField(
        verbose_name='Наименование жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Класс, представляющий произведение."""
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
        through='GenreTitle',
        related_name='titles',
    )
    name = models.CharField(
        verbose_name='Наименование произведения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Дата релиза произведения',
        validators=[validate_year_not_future],
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        default='Нет описания',
        max_length=200,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} {self.genres}'


class GenreTitle(models.Model):
    """Класс, представляющий связь жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр контента',
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'Произведение {self.title} относится к жанру {self.genre}'


class Review(models.Model):
    """Класс, представляющий отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
    )
    text = models.TextField(max_length=1000, blank=False)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        default=1
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text[:FIRST_CHARACTERS_OF_TEXT]


class Comment(models.Model):
    """Класс, представляющий комментарии."""
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

    def __str__(self):
        return self.text[:FIRST_CHARACTERS_OF_TEXT]
