from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView

from .models import Post, Comment, Favorite
from .serializers import PostSerializers, CommentSerializer, FavoriteSerializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        tags = self.request.query_params.getlist('tags')

        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if tags:
            queryset = queryset.filter(tags__name__icontains__in=tags).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        return Response({'message': 'Image uploaded successfully!'})

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False

        else:
            post.likes.add(user)
            liked = True

        post.dislikes.remove(user)

        serializer = self.get_serializer(post)
        return Response({'liked': liked, 'post': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.dislikes.all():
            post.dislikes.remove(user)
            disliked = False
        else:
            post.dislikes.add(user)
            disliked = True
        post.likes.remove(user)
        serializer = self.get_serializer(post)
        return Response({'disliked': disliked, 'post': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        post = Post.objects.get(id=pk)

        favorite, created = Favorite.objects.get_or_create(author=request.user, post=post)
        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'}, status=status.HTTP_200_OK)
        return Response({'status': 'added to favorites'}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteToggleViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [IsAuthenticated]

