from django.urls import include, path
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    UserCreateListViewSet, UserChangeDeleteViewSet,
                    UserMeViewSet, SignUpViewSet, GetTokenViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register('users', UserCreateListViewSet)
router_v1.register(r'users/(?P<username>[\w.@+-]+)/', UserChangeDeleteViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', GetTokenViewSet.as_view({'post': 'create'}),
         name='token_obtain_pair'),
    path('v1/auth/signup/', SignUpViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/users/me/', UserMeViewSet.as_view({'get': 'retrieve',
                                                'patch': 'partial_update'}),
         name='me'),
]
