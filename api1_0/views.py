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
  qLat = request.GET.get('qLat', False)
  qLong = request.GET.get('qLong', False)

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
      laFecha = str(FotoObtenida[0].PhotoPostDateTime)
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
