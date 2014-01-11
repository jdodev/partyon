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
    url(r'^dataheydj/$', views.dataheydj, name='dataheydj'),
    url(r'^postphoto/$', views.postphoto, name='postphoto'),
    url(r'^login/$', views.loginpartyon, name='loginpartyon'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^help/$', views.help, name='help'),
    url(r'^savephotopost/$', views.savephotopost, name='savephotopost'),
    url(r'^savesongpost/$', views.savesongpost, name='savesongpost'),
    url(r'^logout/$', views.logoutpatyon, name='logoutpatyon'),
    url(r'^postsong/$', views.postsong, name='postsong'),
    url(r'^plus/$', views.plus, name='plus'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^update/$', views.update, name='update'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}, ),
)