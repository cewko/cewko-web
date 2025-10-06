from django import template
from apps.weblog.models import Article


register = template.Library()

@register.inclusion_tag("weblog/recent_articles_widget.html")
def recent_articles_widget(limit=5):
    articles = Article.published.all()[:limit]
    return {"articles": articles}