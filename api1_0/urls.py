from django.conf.urls import patterns, url, include
from webapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = patterns('',
    #API
    url(r'^getplaces/$', views.getplaces, name='getplaces'),
    url(r'^datahome/$', views.APIdataHome, name='APIdataHome'),
    url(r'^dataactivity/$', views.APIdataactivity, name='APIdataactivity'),
    url(r'^savephotopost/$', views.APIsavephotopost, name='APIsavephotopost'),
    url(r'^APIsaveplace/$', views.APIsaveplace, name='APIsaveplace'),
    url(r'^login/$', views.APIloginpartyon, name='APIloginpartyon'),
    url(r'^userprofile/$', views.APIuserprofile, name='APIuserprofile'),
    url(r'^updatephotoprofile/$', views.APIupdataphotoprofile, name='APIupdataphotoprofile'),
    url(r'^changepassword/$', views.APIupdatepasswords, name='APIupdatepasswords'),
    url(r'^heydj/$', views.APIheydj, name='APIheydj'),
    url(r'^songpost/$', views.APIsongpost, name='APIsongpost'),
    url(r'^addnewplace/$', views.APIaddplace, name='APIaddplace'),
    url(r'^comprobarusername/$', views.APIcomprobarusername, name='APIcomprobarusername'),
    url(r'^comprobaremail/$', views.APIcomprobaremail, name='APIcomprobaremail'),
    url(r'^addnewuser/$', views.APIsignup, name='APIsignup'),
    url(r'^get9photostiles/$', views.APIget9photostiles, name='APIget9photostiles'),
    url(r'^terms/$', views.APIterms, name='APIterms'),
    url(r'^privacy/$', views.APIprivacy, name='APIprivacy'),
    url(r'^verify/email/$', views.APIverifyemail, name='APIverifyemail'),
    url(r'^verify/sendemail/$', views.APIsendvalidarcorreo, name='APIsendvalidarcorreo'),
)
