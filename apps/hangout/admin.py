from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["nickname", "content_preview", "timestamp", "ip_address", "source"]
    list_filter = ["timestamp", "is_from_discord"]
    search_fields = ["nickname", "content", "discord_user_id"]
    date_hierarchy = "timestamp"
    readonly_fields = ["timestamp", "ip_address", "discord_user_id", "is_from_discord"]
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Message"
    
    def source(self, obj):
        return "Discord" if obj.is_from_discord else "Website"
    source.short_description = "Source"
    
    def has_add_permission(self, request):
        return False