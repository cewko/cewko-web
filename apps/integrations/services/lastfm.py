import requests
from decouple import config
from .base import BaseIntegrationService


class LastFmService(BaseIntegrationService):
    cache_timeout = 5

    def __init__(self):
        self.api_key = config("LASTFM_API_KEY", default="")
        self.username = config("LASTFM_USERNAME", default="")
        self.api_url = "http://ws.audioscrobbler.com/2.0/"

    def get_cache_key(self):
        return f"integration:lastfm:{self.username}"

    def fetch_data(self):
        if not self.api_key or not self.username:
            return None

        try:
            params = {
                "method": "user.getrecenttracks",
                "user": self.username,
                "api_key": self.api_key,
                "format": "json",
                "limit": 1
            }

            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            if "recenttracks" in data and "track" in data["recenttracks"]:
                tracks = data["recenttracks"]["track"]
                track = tracks[0] if isinstance(tracks, list) else tracks
                
                return {
                    "artist": track.get("artist", {}).get("#text", "unknown artist"),
                    "name": track.get("name", "unknown song"),
                }
            
            return None
            
        except requests.RequestException:
            return None
