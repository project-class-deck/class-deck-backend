from django.contrib import admin

from .models import Board, Card, Comment, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = ("title", "author")
    list_filter = ("author",)
    date_hierarchy = "created_at"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("no", "board", "image_front")
    search_fields = ("image_front",)
    list_filter = ("image_front",)
    date_hierarchy = "created_at"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "card", "created_at")
    search_fields = ("title", "author")
    list_filter = ("created_at", "is_public")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content_type", "content_object", "content", "created_at")
    search_fields = ("author", "content", "content_object")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
