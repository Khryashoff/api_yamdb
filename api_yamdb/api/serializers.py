from django.conf import settings
from rest_framework import serializers
from users.models import User
from users.validators import ValidateUsername

from api_yamdb.settings import EMAIL, USERNAME_NAME


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]

class UserEditSerializer(UsersSerializer):
    """Сериализатор модели User для get и patch"""

    role = serializers.CharField(read_only=True)

class RegistrationSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор регистрации User"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    email = serializers.EmailField(required=True, max_length=EMAIL)

class TokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор токена"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    confirmation_code = serializers.CharField(required=True)
