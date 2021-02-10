"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from appp.views import *
from app.views import *
from django.conf.urls.static import static
from django.conf import settings
from app.models import SiteEdit
from app.sitemaps import StaticViewSitemap ,PostSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap
}

urlpatterns = [path('admin/', admin.site.urls),url(r'^see-all/$',
               see_all_notification, name='see_all_notification'),
               path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemap"),]

site = SiteEdit.objects.get(id = 1)
if site.active == False:
    urlpatterns+=[path('', close, name='close'),]
elif site.active == True:
    urlpatterns += [path('', home, name='home'),
                    path('worker/<str:id>', worker, name='worker'),
                    path('client/<str:id>', client, name='client'),
                    path('detail/<str:slug>', post, name='post'),
                    path('blog/', blog, name='blog'),
                    path('about/',about,name='about'),
                    path('contact-us/',contact,name='contact'),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






