from django.core.cache import cache
from .models import Visit


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not request.path.startswith(("/admin/", "/static/", "/media/", "/ws/")):
            ip = self._get_client_ip(request)
            
            cache_key = f"visit_{ip}"
            if not cache.get(cache_key):
                Visit.objects.create(ip_address=ip)
                cache.set(cache_key, True, 300)
        
        return self.get_response(request)
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
        return ip
