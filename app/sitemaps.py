from django.contrib.sitemaps import Sitemap
from .models import *
from django.shortcuts import reverse


class PostSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.8

    def items(self):
        return Posts.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.date




class StaticViewSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.8
    def items(self):
        return ['home','about','blog','contact']
    def location(self, item):
        return reverse(item)