from abc import ABC, abstractmethod
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class BaseIntegrationService(ABC):
    cache_timeout = 300

    @abstractmethod
    def get_cache_key(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    def get_data(self):
        cache_key = self.get_cache_key()
        data = cache.get(cache_key)
        
        if data is None:
            logger.info(f"Cache miss for {cache_key}, fetching data...")
            data = self.fetch_data()
            
            if data is not None:
                cache.set(cache_key, data, self.cache_timeout)
                logger.info(f"Cached data for {cache_key}")
            else:
                logger.warning(f"Failed to fetch data for {cache_key}")
        
        return data