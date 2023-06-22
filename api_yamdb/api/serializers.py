from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from titles.models import Title, Category, Genre

from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для безопасных методов."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для небезопасных методов."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        model = User
        read_only_fields = ('role', )


class TokenSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """Сериализатор токенов пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email')


class SignUpSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """Сериализатор для подтверждения пользователя."""

    class Meta:
        model = User
        fields = ('username', )
