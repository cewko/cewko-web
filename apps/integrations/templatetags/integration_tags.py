from django import template
from apps.integrations.services import DiscordService, LastFmService

register = template.Library()


@register.inclusion_tag("integrations/discord_status.html")
def discord_status_widget():
    service = DiscordService()
    data = service.get_data()

    status = "offline"
    if data:
        status = data["status"]

    return {"status": status}


@register.inclusion_tag('integrations/lastfm_widget.html')
def lastfm_widget():
    service = LastFmService()
    data = service.get_data()
    
    return {'track': data}