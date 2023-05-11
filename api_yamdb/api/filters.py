import django_filters

from reviews.models import Title


class TitleFilter(django_filters.rest_framework.FilterSet):
    """
    Фильтр для TitleViewSet.

    Осуществляется поиск по полям: name, year, category, genre.
        - name: фильтрация по названию произведения (регистронезависимо).
        - year: фильтрация по году выхода произведения.
        - category: фильтрация по slug категории.
        - genre: фильтрация по slug жанра.
    """
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre',)
