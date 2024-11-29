from django.contrib import admin
from .models import Post, Comment, Favorite, Category, Tag


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('title', 'views', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Category)
admin.site.register(Tag)
