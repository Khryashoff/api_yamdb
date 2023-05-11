from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """
    Проверка разрешений для объекта.

    Администраторы обладают всеми правами.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка разрешений для объекта.

    Администраторы обладают всеми правами.
    Остальные пользователи обладают правами только на чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser
            )
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка разрешений для объекта.

    Аутентифицированным пользователям доступно только чтение.
    Аутентифицированные авторы публикаций, модераторы и
    администраторы могут редактировать или удалять их.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )
