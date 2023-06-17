from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CategoryViewSet, GenreViewSet
from users.views import (UserCreateListViewSet,
                         UserChangeDeleteViewSet,
                         UserMeViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register('users', UserCreateListViewSet)
router_v1.register(r'users/(?P<username>[\w.@+-]+)/', UserChangeDeleteViewSet)
router_v1.register('users/me', UserMeViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
