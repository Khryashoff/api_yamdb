from django.db import models

from api_yamdb.settings import NAME_LENGTH, SLUG_LENGTH


class CategoryGenreModel(models.Model):
    """
    Абстрактный базовый класс для моделей Category и Genre.
    """
    name = models.CharField(
        verbose_name='Наименование категории/жанра',
        max_length=NAME_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории/жанра',
        max_length=SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
