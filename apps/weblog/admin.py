from django.contrib import admin
from .models import Article 


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

    
