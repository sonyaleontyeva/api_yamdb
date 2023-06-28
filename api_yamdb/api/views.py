from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from titles.models import Title, Category, Genre
from reviews.models import Review

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (CheckUser, IsAdmin,
                          ReadOnly, IsAdminModeratorOwnerOrReadOnly)
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          SignUpSerializer, TokenSerializer,
                          UserSerializer, CommentSerializer, ReviewSerializer)
from .utils import get_confirmation_code, send_letter


User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (ReadOnly | IsAdmin,)
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
    permission_classes = (ReadOnly | IsAdmin,)


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnly | IsAdmin,)


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
        if serializer.is_valid():
            serializer.save()


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
        confirmation_code = get_confirmation_code(found_user)

        send_letter(email, confirmation_code)

        # found_user.confirmation_code = confirmation_code
        found_user.save()


class TokenViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для отправки токена."""

    serializer_class = TokenSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    # Припоминаю как меня ревьюер ругался за ненужные переменные
    def get_queryset(self):
        """Метод для получения queryset с отзывами."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Метод для сохранения отзыва с автором текущего пользователя."""
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        """Метод для получения объекта Title."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        """Метод для получения queryset с комментариями."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Метод для сохранения комментария с автором текущего пользователя."""
        serializer.save(author=self.request.user, review=self.get_review())

    # У нас ведь и так айдишник уникальный? Зачем еще и title туда передавать
    def get_review(self):
        """Метод для получения объекта Review."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review
