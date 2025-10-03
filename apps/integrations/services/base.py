from abc import ABC, abstractmethod
from django.core.cache import cache


class BaseIntegrationService(ABC):
    cache_timeout = 300

    @abstractmethod
    def get_cache_key(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    def get_data(self, force_fetch = False):
        cache_key = self.get_cache_key()

        if not force_fetch:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            
        data = self.fetch_data()

        if data is not None:
            cache.set(cache_key, data, self.cache_timeout)

        return data