from django.conf.urls import patterns, url
from webapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^datahome/$', views.datahome, name='datahome'),
    url(r'^datatrends/$', views.datatrends, name='datatrends'),
    url(r'^dataactivity/$', views.dataactivity, name='dataactivity'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}, ),
)