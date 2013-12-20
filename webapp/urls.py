from django.conf.urls import patterns, url
from webapp import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
)