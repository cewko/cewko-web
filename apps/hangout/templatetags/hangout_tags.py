from django import template

register = template.Library()


@register.inclusion_tag('hangout/hangout_widget.html')
def hangout_widget():
    return {}