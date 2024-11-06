from rest_framework import serializers
from .models import Post


class PostSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'total_likes']

    def get_total_likes(self, obj):
        return obj.total_likes()

