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


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
