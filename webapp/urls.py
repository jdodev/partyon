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
    url(r'^songpostpointadd/$', views.songpostpointadd, name='songpostpointadd'),
    url(r'^songpostpointdel/$', views.songpostpointdel, name='songpostpointdel'),
    url(r'^savenewplace/$', views.savenewplace, name='savenewplace'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}, ),



    #API
    url(r'^API/getplaces/$', views.getplaces, name='getplaces'),
    url(r'^API/datahome/$', views.APIdataHome, name='APIdataHome'),
    url(r'^API/dataactivity/$', views.APIdataactivity, name='APIdataactivity'),
    url(r'API/savephotopost/$', views.APIsavephotopost, name='APIsavephotopost'),
    url(r'API/APIsaveplace/$', views.APIsaveplace, name='APIsaveplace'),
    url(r'API/login/$', views.APIloginpartyon, name='APIloginpartyon'),
    url(r'API/userprofile/$', views.APIuserprofile, name='APIuserprofile'),
    url(r'API/updatephotoprofile/$', views.APIupdataphotoprofile, name='APIupdataphotoprofile'),
    url(r'API/changepassword/$', views.APIupdatepasswords, name='APIupdatepasswords'),
    url(r'API/heydj/$', views.APIheydj, name='APIheydj'),
    url(r'API/songpost/$', views.APIsongpost, name='APIsongpost'),
    url(r'API/addnewplace/$', views.APIaddplace, name='APIaddplace'),
    url(r'API/comprobarusername/$', views.APIcomprobarusername, name='APIcomprobarusername'),
    url(r'API/comprobaremail/$', views.APIcomprobaremail, name='APIcomprobaremail'),
)