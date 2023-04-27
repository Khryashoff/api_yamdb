from django.db import models
from users.models import User

from .validators import validate_year_not_future


class Category(models.Model):

    pass


class Genre(models.Model):

    pass


class Title(models.Model):
    """Класс, представляющий произведение."""
    category = models.ForeignKey(
        Category,
        verbose_name='Категория контента',
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр контента',
        related_name='titles',
        blank=True,
    )
    name = models.CharField(
        verbose_name='Наименование произведения',
        max_length=150,
    )
    year = models.IntegerField(
        verbose_name='Дата релиза произведения',
        validators=[validate_year_not_future],
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
