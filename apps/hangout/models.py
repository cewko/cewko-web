from django.db import models
from django.utils import timezone


class Message(models.Model):
    nickname = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.nickname}: {self.content[:50]}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
        }