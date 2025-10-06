import re
import html
import requests
from datetime import datetime
from decouple import config
from django.utils.html import strip_tags
from .base import BaseIntegrationService


class MastodonService(BaseIntegrationService):
    cache_timeout = 3600

    def __init__(self):
        self.instance = config("MASTODON_INSTANCE", default="")
        self.username = config("MASTODON_USERNAME", default="")
        self.api_url = f"https://{self.instance}/api/v1"

    def get_cache_key(self):
        return f"integration:mastodon:{self.username}"

    def fetch_data(self):
        if not self.instance or not self.username:
            return None

        try:
            account_url = f"{self.api_url}/accounts/lookup"
            account_params = {"acct": self.username}
        
            account_response = requests.get(
                account_url,
                params=account_params,
                timeout=5
            )
            account_response.raise_for_status()
            account_data = account_response.json()
            account_id = account_data['id']

            statuses_url = f"{self.api_url}/accounts/{account_id}/statuses"
            statuses_params = {
                "limit": 1,
                "exclude_replies": "true",
                "exclude_reblogs": "false"
            }

            statuses_response = requests.get(
                statuses_url,
                params=statuses_params,
                timeout=5
            )
            statuses_response.raise_for_status()
            statuses = statuses_response.json()
            
            if not statuses:
                return None

            status = statuses[0]

            created_at = datetime.fromisoformat(
                status["created_at"].replace("Z", "+00:00")
            )

            content = status['content']
            content = re.sub(r'<a[^>]*href="[^"]*"[^>]*>.*?</a>', '[link] ', content, flags=re.DOTALL)
            content = strip_tags(content)
            content = html.unescape(content)
            
            media_text = ""
            if status.get("media_attachments"):
                media_counts = {}
                for media in status["media_attachments"]:
                    media_type = media["type"]
                    media_counts[media_type] = media_counts.get(media_type, 0) + 1

                media_parts = []
                for media_type, count in media_counts.items():
                    if count == 1:
                        if media_type == 'image':
                            media_parts.append('[image]')
                        elif media_type == 'video':
                            media_parts.append('[video]')
                        elif media_type == 'gifv':
                            media_parts.append('[gif]')
                        elif media_type == 'audio':
                            media_parts.append('[audio]')
                    else:
                        if media_type == 'image':
                            media_parts.append(f'[{count} images]')
                        elif media_type == 'video':
                            media_parts.append(f'[{count} videos]')
                        elif media_type == 'gifv':
                            media_parts.append(f'[{count} gifs]')
                        elif media_type == 'audio':
                            media_parts.append(f'[{count} audios]')
                
                if media_parts:
                    content = content + ' ' + ' '.join(media_parts)

            return {
                'content': content,
                'url': account_data["url"],
                'created_at': created_at,
                'username': account_data['username'],
                'avatar': account_data['avatar'],
            }

        except requests.Timeout:
            return None
        except requests.RequestException as e:
            return None
        except (KeyError, ValueError, TypeError) as e:
            return None