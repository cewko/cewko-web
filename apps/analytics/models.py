from django.db import models
from django.utils import timezone
from datetime import timedelta


class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
    
    @classmethod
    def get_stats(cls):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        five_min_ago = now - timedelta(minutes=5)
        
        return {
            'total_visits': cls.objects.count(),
            'unique_visitors': cls.objects.values('ip_address').distinct().count(),
            'today_visits': cls.objects.filter(timestamp__gte=today_start).count(),
            'online_now': cls.objects.filter(timestamp__gte=five_min_ago).values('ip_address').distinct().count(),
        }