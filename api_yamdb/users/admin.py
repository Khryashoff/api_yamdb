from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from users.models import User


@admin.register(User)
class CategoriesAdmin(UserAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_active'].help_text = 'Статус - пользователь'
        form.base_fields['is_superuser'].help_text = 'Статус - администратор'
        return form

    list_display = (
        'username',
        'email',
        'is_staff',
        'role',
        'date_joined',
    )
    search_fields = ('username',)
    list_filter = ('username',)
    list_editable = ('is_staff', 'role',)
    empty_value_display = '-пусто-'

    ordering = ['role']
    fieldsets = (
        (
            'Пользовательские данные',
            {'fields': ('username', 'email', 'date_joined',)}
        ),
        (
            'Администраторские полномочия',
            {'fields': ('is_active', 'role', 'is_superuser',)}
        ),
    )
