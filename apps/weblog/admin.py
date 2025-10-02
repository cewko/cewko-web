from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "published_at", "created_at"]
    list_filter = ["status", "created_at", "published_at"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]

    fieldsets = (
        ("Content", {
            "fields": (
                "title", "slug", "body"
            ),
        }),
        ("Metadata", {
            "fields": (
                "status",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "published_at", "created_at", "updated_at"
            ),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ["created_at", "updated_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["nickname", "article", "created_at", "body_preview"]
    list_filter = ["created_at"]
    search_fields = ["nickname", "body", "article__title"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    
    def body_preview(self, obj):
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body
    body_preview.short_description = "Comment Preview"
