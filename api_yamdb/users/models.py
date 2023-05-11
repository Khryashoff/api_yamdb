from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from api_yamdb.settings import EMAIL, USERNAME_NAME

from users.validators import ValidateUsername


class User(AbstractUser, ValidateUsername):
    """Класс, представляющий пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        verbose_name='Никнейм пользователя',
        max_length=USERNAME_NAME,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        validators=[validate_email],
        max_length=EMAIL,
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
        max_length=max([len(role) for role, name in ROLES]),
        choices=ROLES,
        default=USER,
    )

    # @property
    # def is_user(self):
    #     return True if not self.is_staff else None

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
