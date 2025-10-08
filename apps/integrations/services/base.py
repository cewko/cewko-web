from abc import ABC, abstractmethod
from django.core.cache import cache


class BaseIntegrationService(ABC):
    cache_timeout = 300

    @abstractmethod
    def get_cache_key(self):
        """Return the cache key for this service"""
        pass

    @abstractmethod
    def fetch_data(self):
        """Fetch fresh data from the external API"""
        pass

    def get_data(self, force_fetch=False):
        if force_fetch:
            from apps.integrations.tasks import (
                refresh_discord_status,
                refresh_lastfm_track,
                refresh_weather_data,
                refresh_wakatime_stats,
                refresh_mastodon_status,
                refresh_github_contributions
            )

            task_map = {
                "integration:discord": refresh_discord_status,
                "integration:lastfm": refresh_lastfm_track,
                "integration:weather": refresh_weather_data,
                "integration:wakatime": refresh_wakatime_stats,
                "integration:mastodon": refresh_mastodon_status,
                "integration:github": refresh_github_contributions,
            }

            cache_key = self.get_cache_key()
            prefix = cache_key.rsplit(":", 1)[0] if ":" in cache_key else cache_key

            for key_prefix, task in task_map.items():
                if cache_key.startswith(key_prefix):
                    task.delay()
                    break

        cache_key = self.get_cache_key()
        return cache.get(cache_key)
