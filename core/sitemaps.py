from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.weblog.models import Article


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "yearly"
    protocol = "https"

    def items(self):
        return ["pages:home", "pages:about"]

    def location(self, item):
        return reverse(item)


class WeblogSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return ["weblog:article_inventory"]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    priority = 0.9
    changefreq = "never"
    protocol = "https"

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return reverse("weblog:article_page", args=[obj.slug])


sitemaps = {
    "static": StaticViewSitemap,
    "weblog": WeblogSitemap,
    "articles": ArticleSitemap,
}