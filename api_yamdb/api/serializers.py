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
    # С этим уже после отзывов
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


# Все что придумал это еще один сериализатор для опасных методов.
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

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('first_name должен содержать не '
                                              'более 150 символов!')
        return value

    def validate_last_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('last_name должен содержать не '
                                              'более 150 символов!')
        return value

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое значение '
                                              'username!')
        return value


class SignUpSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """Сериализатор для подтверждения пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if (User.objects.get(username=data.get('username'))
                and not User.objects.get(email=data.get('email'))):
            raise serializers.ValidationError('Недопустимое значение '
                                              'username!')

        if (User.objects.get(email=data.get('email'))
                and not User.objects.get(username=data.get('username'))):
            raise serializers.ValidationError('Недопустимое значение '
                                              'email!')
        return data

    # def validate_username(self, value):
    #     if User.objects.get(username=value):
    #         raise serializers.ValidationError('Недопустимое значение '
    #                                           'username!')
    #     return value

    # def validate_email(self, value):
    #     if User.objects.get(email=value):
    #         raise serializers.ValidationError('Недопустимое значение '
    #                                           'email!')
    #     return value
