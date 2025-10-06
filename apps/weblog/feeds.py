from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from .models import Article


class LatestArticlesFeed(Feed):
    title = "cewko's weblog"
    link = reverse_lazy("weblog:article_inventory")
    description = "Latest articles from cewko's weblog"

    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_body_html()

    def item_link(self, item):
        return reverse("weblog:article_page", args=[item.slug])

    def item_pubdate(self, item):
        return item.published_at