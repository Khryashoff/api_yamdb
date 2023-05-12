from api_yamdb.settings import REGEX_USERNAME
from django.core.exceptions import ValidationError


class ValidateUsername:
    """
    Валидатор для username.
    """
    def validate_username(self, username):
        if not REGEX_USERNAME.fullmatch(username):
            raise ValidationError(
                f'Некорректные символы в username: {REGEX_USERNAME}'
            )
        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username
