from django.contrib import admin
from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'timestamp']
    list_filter = ['timestamp']
    date_hierarchy = 'timestamp'
    readonly_fields = ['ip_address', 'timestamp']
    
    def has_add_permission(self, request):
        return False