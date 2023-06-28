from django.urls import include, path
from rest_framework import routers

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    UserCreateListViewSet, UserChangeDeleteViewSet,
                    UserMeViewSet, SignUpViewSet, TokenViewSet,
                    ReviewViewSet, CommentViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register('users', UserCreateListViewSet)
router_v1.register(r'users/(?P<username>[\w.@+-]+)/', UserChangeDeleteViewSet)
router_v1.register('users/me', UserMeViewSet)
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='token')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
