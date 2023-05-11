import re

from django.core.exceptions import ValidationError

REGEX_USERNAME = re.compile(r'^[\w.@+-]+')

class ValidateUsername:
    """Валидаторы для username."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+\Z')

        if not REGEX_USERNAME.fullmatch(username):
            raise ValidationError(f'Некорректные символы в username: {REGEX_USERNAME}')
        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username