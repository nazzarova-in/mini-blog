from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializers, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

