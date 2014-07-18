# -*- encoding: utf-8 -*-
from datetime import datetime, date, timedelta
from django.core import serializers
from django.db.models import Count, Max, Sum, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from webapp.models import *
from webapp.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.mail import EmailMessage
import json

def APIdataHome(request):
  qLat = request.GET.get('qLat')
  qLong = request.GET.get('qLong')

  #Sumamos los valores del marge de error
  qLatMax = float(qLat) + 0.2000000
  qLatMin = float(qLat) - 0.2000000

  qLongMax = float(qLong) + 0.2000000
  qLongMin = float(qLong) - 0.2000000

  hoy = date.today()
  ayer = hoy - timedelta(1)
  manana = hoy + timedelta(1)

  resPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= '  + str(qLatMin) + ' AND PlaceLong <= ' + str(qLongMax) + ' AND PlaceLong >= ' + str(qLongMin)]).order_by('PlaceName')[:70]

  lstPlacePhotos = []

  for dPlace in resPlaces:
    hayFoto = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID').count()
    if hayFoto > 0:
      FotoObtenida = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID')[:1]
      laFoto = str(FotoObtenida[0].PhotoPostPhoto)
      laFecha = naturaltime(FotoObtenida[0].PhotoPostDateTime)
    else:
      laFoto = 'PhotoPosts/nofoto.jpg'
      laFecha = "No Data"

    totPersonas = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).count()
    dctLugares = {
    "PlaceID":dPlace.PlaceID,
    "PlaceName":dPlace.PlaceName,
    "PlaceLat":dPlace.PlaceLat,
    "PlaceLong":dPlace.PlaceLong,
    "PlaceLogo":str(dPlace.PlaceLogo),
    "LastPhoto":laFoto,
    "LastPostDate":laFecha,
    "PeopleNow":totPersonas,
    }
    lstPlacePhotos.append(dctLugares)

  respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstPlacePhotos}
  return HttpResponse(json.dumps(respuesta), content_type='application/json')


def APIdataactivity(request):
  resUserActivity = PhotoPost.objects.select_related('user__userprofile').order_by('-PhotoPostID')[:25]

  lstActivity = []

  for act in resUserActivity:
    timesince_c = naturaltime(act.PhotoPostDateTime)
    dctActivity = {
    'PhotoPhostID':act.PhotoPostID,
    'PhotoPostDateTime':act.PhotoPostDateTime.strftime('%Y-%m-%d %H:%M'),
    'PhotoPostTimeSince':timesince_c,
    'PhotoPost_PlaceID':act.PhotoPost_PlaceID.PlaceID,
    'PhotoPost_PlaceName':act.PhotoPost_PlaceID.PlaceName,
    'PhotoPost_PlaceLat':act.PhotoPost_PlaceID.PlaceLat,
    'PhotoPost_PlaceLong':act.PhotoPost_PlaceID.PlaceLong,
    'PhotoPostPhoto':str(act.PhotoPostPhoto),
    'PhotoPost_UserProfileID':act.PhotoPost_User.UserProfileID,
    'PhotoPost_UserID':act.PhotoPost_User.UserProfile_User.pk,
    'PhotoPost_UserName':act.PhotoPost_User.UserProfile_User.username,
    'PhotoPost_UserFirstName':act.PhotoPost_User.UserProfile_User.first_name,
    'PhotoPost_UserLastName':act.PhotoPost_User.UserProfile_User.last_name,
    'PhotoPost_UserAvatar':str(act.PhotoPost_User.UserProfilePhoto),
    'PhotoPost_Lat':act.PhotoPost_Lat,
    'PhotoPostLong':act.PhotoPostLong,
    'PhotoPostDescription':act.PhotoPostDescription,
    }
    lstActivity.append(dctActivity)

  respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstActivity}
  return HttpResponse(json.dumps(respuesta), content_type='application/json')


def APIheydj(request):
  qLat = request.GET.get('qLat', False)
  qLong = request.GET.get('qLong', False)

  #Sumamos los valores del marge de error
  qLatMax = float(qLat) + 0.0020000
  qLatMin = float(qLat) - 0.0020000

  qLongMax = float(qLong) + 0.0020000
  qLongMin = float(qLong) - 0.0020000

  resHeyDj = SongPost.objects.extra(where=['SongPostLat <= ' + str(qLatMax) + ' AND SongPostLat >= '  + str(qLatMin) + ' AND SongPostLong <= ' + str(qLongMax) + ' AND SongPostLong >= ' + str(qLongMin)]).order_by('-SongPostID')[:25]

  lstHeyDj = []

  for song in resHeyDj:
    timesince_c = naturaltime(song.SongPostDateTime)
    dctHeyDj = {
    "SongPostID":song.SongPostID,
    "SongPostDateTime":song.SongPostDateTime.strftime('%Y-%m-%d %H:%M'),
    "SongPostTimeSince":timesince_c,
    "SongPost_PlaceID":song.SongPost_PlaceID.PlaceID,
    "PlaceName":song.SongPost_PlaceID.PlaceName,
    "SongPostName":song.SongPostName,
    "SongPost_User":song.SongPost_User.UserProfile_User.id,
    "Username":song.SongPost_User.UserProfile_User.username,
    "UserFirstName":song.SongPost_User.UserProfile_User.first_name,
    "UserLastName":song.SongPost_User.UserProfile_User.last_name,
    "SongPostLat":song.SongPostLat,
    "SongPostLong":song.SongPostLong,
    "SongPostQuote":song.SongPostQuote,
    }
    lstHeyDj.append(dctHeyDj)

  respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstHeyDj}
  return HttpResponse(json.dumps(respuesta), content_type='application/json')
