from django import template
from apps.analytics.models import Visit

register = template.Library()


@register.inclusion_tag('analytics/stats_widget.html')
def analytics_widget():
    return Visit.get_stats()