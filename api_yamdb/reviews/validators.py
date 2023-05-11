from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year_not_future(year: int) -> None:
    """
    Проверяет указанный год на соответствие параметрам.
    """
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError('Год не может быть больше текущего года.')
