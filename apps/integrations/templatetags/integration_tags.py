from django import template
from apps.integrations.services import DiscordService

register = template.Library()


@register.inclusion_tag("integrations/discord_status.html")
def discord_status_widget():
    service = DiscordService()
    data = service.get_data()

    status = "offline"
    if data:
        status = data["status"]

    return {"status": status}