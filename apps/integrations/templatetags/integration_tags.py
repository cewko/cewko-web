from django import template
from apps.integrations.services import (
    DiscordService, 
    LastFmService, 
    WeatherService,
    WakatimeService,
    MastodonService,
    GithubService
)

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


@register.inclusion_tag('integrations/weather_widget.html')
def weather_widget():
    service = WeatherService()
    data = service.get_data()
    
    return {'weather': data}


@register.inclusion_tag('integrations/wakatime_widget.html')
def wakatime_widget():
    service = WakatimeService()
    data = service.get_data()
    
    return {'stats': data}


@register.inclusion_tag("integrations/mastodon_widget.html")
def mastodon_widget():
    service = MastodonService()
    data = service.get_data()

    return {"status": data}


@register.inclusion_tag("integrations/github_widget.html")
def github_widget():
    service = GithubService()
    data = service.get_data()

    return {"github": data}