from django.urls import path
from . import views
from .feeds import LatestArticlesFeed


app_name = "weblog"

urlpatterns = [
    path("", views.article_inventory, name="article_inventory"),
    path("rss/", LatestArticlesFeed(), name="rss_feed"),
    path("<slug:slug>/", views.article_page, name="article_page")
]
