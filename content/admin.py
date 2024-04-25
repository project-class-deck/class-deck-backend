from django.contrib import admin

from .models import Board, Card, Comment, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "owner")
    search_fields = ("title", "owner")
    list_filter = ("owner",)
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
    list_display = ("user", "content_type", "content_object", "text", "created_at")
    search_fields = ("user", "text", "content_object")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
