from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from titles.models import Title, Category, Genre
from users.models import User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import CheckUser, IsAdmin
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          SignUpSerializer, TokenSerializer,
                          UserSerializer)
from .utils import get_confirmation_code, send_letter


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Метод для определения класса сериализатора."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserCreateListViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """Вьюсет для создания одного пользователя и вывода списка
    пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticated)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def perform_create(self, serializer):
        serializer.save(role='user')


class UserChangeDeleteViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Вьюсет для изменения и удаления пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticated)
    http_method_names = ['get', 'patch', 'delete']

    def retrieve(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)


class UserMeViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для просмотра и изменения данных своего пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CheckUser, IsAuthenticated)
    http_method_names = ['get', 'patch']

    def retrieve(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        instance = get_object_or_404(self.queryset, username=username)
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для регистрации с отправкой кода подтверждения по email."""

    serializer_class = SignUpSerializer

    def create(self, request, username=None, email=None):
        found_user = get_object_or_404(self.queryset, username=username,
                                       email=email)
        confirmation_code = get_confirmation_code()

        send_letter(email, confirmation_code)

        # found_user.confirmation_code = confirmation_code
        found_user.save()


class TokenViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для отправки токена."""

    serializer_class = TokenSerializer
