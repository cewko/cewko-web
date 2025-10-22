"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import (
    StaticViewSitemap, 
    WeblogSitemap, 
    ArticleSitemap,
)
from core.sitemaps import sitemaps


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.pages.urls")),
    path("weblog/", include("apps.weblog.urls")),
    path("sitemap.xml/", sitemap, {
        "sitemaps": sitemaps
        }, name="django.contrib.sitemaps.views.sitemap")
]

handler404 = "apps.pages.views.custom_404"

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()