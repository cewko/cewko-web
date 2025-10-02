from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Database
# Using SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Development-specific settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show detailed error pages
DEBUG = True

# Allow all internal IPs for debug toolbar (if you add it later)
INTERNAL_IPS = [
    "127.0.0.1",
]