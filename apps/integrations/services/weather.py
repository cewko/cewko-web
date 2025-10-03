import requests
from django.utils import timezone
import zoneinfo
from .base import BaseIntegrationService


class WeatherService(BaseIntegrationService):
    cache_timeout = 21600

    def __init__(self):
        # warsaw coordinates
        self.latitude = 52.2297
        self.longitude = 21.0122
        self.api_url = 'https://api.open-meteo.com/v1/forecast'
        self.warsaw_tz = zoneinfo.ZoneInfo('Europe/Warsaw')

    def get_cache_key(self):
        return f"integration:weather:warsaw"

    def fetch_data(self):
        try:
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'current': 'temperature_2m,relative_humidity_2m,weather_code',
                'timezone': 'Europe/Warsaw'
            }

            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            current = data["current"]

            warsaw_time = timezone.now().astimezone(self.warsaw_tz)
            weather_description = self._get_weather_description(current['weather_code'])

            return {
                'temperature': round(current['temperature_2m']),
                'humidity': current['relative_humidity_2m'],
                'description': weather_description,
                'time': warsaw_time.strftime('%H:%M'),
                'date': warsaw_time.strftime('%Y-%m-%d'),
                'timezone': 'Europe/Warsaw',
            }
        except requests.RequestException:
            return None
        except Exception:
            return None

    def _get_weather_description(self, code):
        weather_codes = {
            0: 'Clear sky',
            1: 'Mainly clear',
            2: 'Partly cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Foggy',
            51: 'Light drizzle',
            53: 'Moderate drizzle',
            55: 'Dense drizzle',
            61: 'Slight rain',
            63: 'Moderate rain',
            65: 'Heavy rain',
            71: 'Slight snow',
            73: 'Moderate snow',
            75: 'Heavy snow',
            77: 'Snow grains',
            80: 'Slight rain showers',
            81: 'Moderate rain showers',
            82: 'Violent rain showers',
            85: 'Slight snow showers',
            86: 'Heavy snow showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with hail',
            99: 'Thunderstorm with hail',
        }
        return weather_codes.get(code, 'unknown')
