from django.contrib import admin

from reviews.models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'category',
        'name',
        'year',
        'description',
    )
    list_editable = ('category',)
    list_filter = ('genre', 'category')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
