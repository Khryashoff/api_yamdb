from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class SignupSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        min_length=2,
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def validate(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Пользователь с таким username уже существует')
        if username == 'me':
            raise serializers.ValidationError("Имя пользователя 'me' запрещено.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return validated_data


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        input_confirmation_code = data.get('confirmation_code')
        if input_confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Некорректный код подтверждения.'
            )
        return data

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
