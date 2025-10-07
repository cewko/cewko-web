from django.db import models
from django.utils import timezone
from datetime import timedelta
import redis
from decouple import config


class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ["-timestamp"]
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
    
    @classmethod
    def get_stats(cls):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        online_count = cls.get_online_count_from_redis()
        
        return {
            "total_visits": cls.objects.count(),
            "unique_visitors": cls.objects.values("ip_address").distinct().count(),
            "today_visits": cls.objects.filter(timestamp__gte=today_start).count(),
            "online_now": online_count,
        }
    
    @classmethod
    def get_online_count_from_redis(cls):
        try:
            redis_client = redis.from_url(
                config("REDIS_URL", default="redis://localhost:6379")
            )
            online_users = redis_client.scard("online_users")
            redis_client.close()
            return online_users
        except Exception as e:
            print(f"Redis error: {e}")
            return 0
