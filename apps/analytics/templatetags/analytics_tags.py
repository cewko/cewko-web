from django import template
from apps.analytics.models import Visit

register = template.Library()


@register.inclusion_tag('analytics/visitors_widget.html')
def visitors_widget():
    stats = Visit.get_stats()
    return {
        'total_visits': stats['total_visits'],
        'unique_visitors': stats['unique_visitors'],
    }