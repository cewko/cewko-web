from django.db import models


class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ["-timestamp"]
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
    
    @classmethod
    def get_stats(cls):
        return {
            "total_visits": cls.objects.count(),
            "unique_visitors": cls.objects.values("ip_address").distinct().count(),
        }