from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from titles.models import Title, Category, Genre
from users.models import User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import CheckUser, IsAdmin
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          SignUpSerializer, UserSerializer,
                          TokenObtainPairSerializer)
from .utils import (get_confirmation_code,
                    check_confirmation_code,
                    send_letter)


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
    permission_classes = (IsAuthenticated, IsAdmin)
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
    permission_classes = (IsAuthenticated, IsAdmin)
    http_method_names = ['get', 'patch', 'delete']

    def retrieve(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        if serializer.is_valid():
            serializer.save()


class UserMeViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для просмотра и изменения данных своего пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, CheckUser)
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
    permission_classes = (AllowAny, )
    queryset = User.objects.all()

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_user, _ = User.objects.get_or_create(
            username=self.request.data.get('username'),
            email=self.request.data.get('email')
        )
        confirmation_code = get_confirmation_code(found_user)

        send_letter(self.request.data.get('email'), confirmation_code)

        # found_user.confirmation_code = confirmation_code
        # found_user.save()
        serializer = self.serializer_class(found_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для получения токена аутентификации."""

    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny, )
    queryset = User.objects.all()

    def create(self, request):
        user_confirmed = check_confirmation_code(
            self.request.data.get('username'),
            self.request.data.get('confirmation_code')
        )

        if user_confirmed:
            serializer = self.serializer_class
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
