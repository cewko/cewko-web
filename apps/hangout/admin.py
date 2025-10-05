from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'content_preview', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['nickname', 'content']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp', 'ip_address']
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Message"
    
    def has_add_permission(self, request):
        return False