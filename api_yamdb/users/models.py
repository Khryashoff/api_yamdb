from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    """Класс, представляющий пользователя."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        verbose_name='Никнейм пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        validators=[validate_email],
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Полномочия доступа',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
