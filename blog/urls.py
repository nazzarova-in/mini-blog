from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FavoriteToggleViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'favorite', FavoriteToggleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]