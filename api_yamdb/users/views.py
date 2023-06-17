from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import User
from .permissions import CheckUser, IsAdmin
from .serializers import UserSerializer


class UserCreateListViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def perform_create(self, serializer):
        serializer.save(role='user')


class UserChangeDeleteViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, IsAuthenticatedOrReadOnly]
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CheckUser, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'patch']

    def retrieve(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        found_user = get_object_or_404(self.queryset, username=username)
        serializer = self.serializer_class(found_user)
        return Response(serializer.data)
