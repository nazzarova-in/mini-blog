from rest_framework import serializers
from .models import Post, Comment, Favorite, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'post', 'image']
        read_only_fields = ['post', 'created_at']


class PostSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'total_likes', 'total_dislikes', 'comments', 'category',
                  'tags', 'image', 'views']

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_dislikes(self, obj):
        return obj.total_dislikes()


class FavoriteSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Favorite
        fields = '__all__'




