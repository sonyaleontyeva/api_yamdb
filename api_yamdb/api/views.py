from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from titles.models import Title, Category, Genre
from users.models import User
from reviews.models import Review

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (CheckUser, IsAdmin,
                          IsAdminModeratorOwnerOrReadOnly)
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          SignUpSerializer, TokenSerializer,
                          UserSerializer, CommentSerializer, ReviewSerializer)
from .utils import get_confirmation_code, send_letter


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
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
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title__id=title_id)
        return review
