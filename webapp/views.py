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
from models import *
from webapp.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
import json


def index(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/home/')
	else:
		loginForm = AuthenticationForm()
		return render(request, 'login.html', {'loginForm' : loginForm})
		#return (HttpResponseRedirect('/admin/'))

def loginpartyon(request):
	loginForm = AuthenticationForm()
	if request.is_ajax():
		if request.method == 'POST':
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				login(request, acceso)
				respuesta = {'codigo': 1, 'msg': 'Welcome to partyon'}
				return HttpResponse(json.dumps(respuesta))
				#return HttpResponseRedirect('/')
			else:
				respuesta = {'codigo': 2, 'msg': 'You have entered an incorrect email or password.'}
				return HttpResponse(json.dumps(respuesta))
				#return render(request, 'login.html', {'loginForm' : loginForm})
		else:
			return render(request, 'login.html', {'loginForm' : loginForm})
	else:
		return render(request, 'login.html', {'loginForm' : loginForm})

@login_required(login_url='/')
def logoutpatyon(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/')
def savephotopost(request):
	if request.method == 'POST':
		formPhotoPost = PhotoPostForm(request.POST, request.FILES)
		if formPhotoPost.is_valid():
			u = formPhotoPost.save(commit=False)
			u.PhotoPostDateTime = datetime.now()
			u.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/novalid/')
	else:
		return HttpResponseRedirect('/nopost/')

@login_required(login_url='/')
def savesongpost(request):
	if request.method == 'POST':
		formSongPost = SongPostForm(request.POST)
		if formSongPost.is_valid():
			u = formSongPost.save(commit=False)
			u.SongPostDateTime = datetime.now()
			u.save()

			VotarAuto = SongPoint(SongPoint_SongPostID=u, SongPoint_User=request.user)
			VotarAuto.save()

			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/novalid/')
	else:
		return HttpResponseRedirect('/nopost/')

def novalido(request):
	formPhotoPost = PhotoPostForm()
	return render(request, 'novalidod.html', {'form' : formPhotoPost})
 
@login_required(login_url='/')
def savenewplace(request):
	if request.is_ajax():
		NewPlace = Place(PlaceName=request.POST['PlaceName'], PlaceLat=request.POST['PlaceLat'], PlaceLong=request.POST['PlaceLong'])
		NewPlace.save()

		respuesta = {'codigo': 1, 'msg': 'Salvado'}
		return HttpResponse(json.dumps(respuesta))
	else:
		respuesta = {'codigo': 1, 'msg': 'No Salvado'}
		return HttpResponse(json.dumps(respuesta))

#Este invoca a la base con las cargas asíncronas
@login_required(login_url='/')
def home(request):
	return render(request, 'home.html')

@login_required(login_url='/')
def datahome(request):
	if request.is_ajax():
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

		resPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= '  + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)])[:10]

		resPersonas = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= ' + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)]).filter(photopost__PhotoPostDateTime__range=[hoy, manana]).annotate(tPersonas=Count('photopost__PhotoPostID'))[:10]

		resPlacePhotos = []

		for dPlace in resPlaces:
			FotoObtenida = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID')[:1]
			resPlacePhotos.append(FotoObtenida)

		return render(request, 'datahome.html', {'TPlaces' : resPlaces, 'TPhotosPlace' : resPlacePhotos, 'TCount' : resPersonas})

@login_required(login_url='/')
def datatrends(request):
	if request.is_ajax():
		resPlaces = Place.objects.all()
		return render(request, 'datatrends.html', {'TPlaces' : resPlaces})

@login_required(login_url='/')
def dataactivity(request):
	if request.is_ajax():
		resUserActivity = PhotoPost.objects.select_related('user__userprofile').order_by('-PhotoPostID')
		return render(request, 'dataactivity.html', {'TUserActivity' : resUserActivity})

@login_required(login_url='/')
def dataheydj(request):
	#if request.is_ajax():
	resHeyDj = SongPost.objects.all().annotate(tVotosSong=Count('songpoint__SongPoint_SongPostID')).order_by('-SongPostID')[:20]

	resTotalVotos = []

	for heyCancion in resHeyDj:
		ConteoObtenido = SongPoint.objects.filter(SongPoint_SongPostID=heyCancion, SongPoint_User=request.user)[:1]
		resTotalVotos.append(ConteoObtenido)

	return render(request, 'dataheydj.html', {'THeyDj' : resHeyDj, 'TVotoUsuario' : resTotalVotos})

@login_required(login_url='/')
def postphoto(request):
	# if request.is_ajax():
	qLat = request.GET.get('qLat', False)
	qLong = request.GET.get('qLong', False)

	#Sumamos los valores del marge de error
	qLatMax = float(qLat) + 0.0020000
	qLatMin = float(qLat) - 0.0020000

	qLongMax = float(qLong) + 0.0020000
	qLongMin = float(qLong) - 0.0020000

	#resNearPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= ' + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)])
	resNearPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= ' + str(qLatMin) + ' AND PlaceLong <= ' + str(qLongMax) + ' AND PlaceLong >= ' + str(qLongMin)])
	return render(request, 'postphoto.html', {'NearPlaces' : resNearPlaces})

@login_required(login_url='/')
def settings(request):
	return render(request, 'settings.html')

@login_required(login_url='/')
def help(request):
	return render(request, 'help.html')

def signup(request):
	if request.method == 'POST':
		frmNewUser = SignUpForm(request.POST)

		if frmNewUser.is_valid():
			firstname = frmNewUser.cleaned_data['first_name']
			lastname = frmNewUser.cleaned_data['last_name']
			email = frmNewUser.cleaned_data['email']
			Username = frmNewUser.cleaned_data['username']
			Password = frmNewUser.cleaned_data['password']

			user = User.objects.create_user(Username, email, Password)
			user.first_name = firstname
			user.last_name = lastname

			user.save()

			ojUsuario = User.objects.get(username=Username)

			PerfilUsuario = UserProfile(UserProfileID=ojUsuario.id, UserProfile_User=ojUsuario, UserProfileMailVerified=False)
			PerfilUsuario.save()

			acceso = authenticate(username=Username, password=Password)
			if acceso is not None:
				login(request, acceso)
				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/NoAcceso')
		else:
			return HttpResponseRedirect('/novalido')
	else:
		return render(request, 'signup.html')

@login_required(login_url='/')
def update(request):
	return render(request, 'update.html')

@login_required(login_url='/')
def postsong(request):
	if request.is_ajax():
		qLat = request.GET.get('qLat', False)
		qLong = request.GET.get('qLong', False)

		#Sumamos los valores del marge de errorsss
		qLatMax = float(qLat) + 0.0020000
		qLatMin = float(qLat) - 0.0020000

		qLongMax = float(qLong) + 0.0020000
		qLongMin = float(qLong) - 0.0020000

		resNearPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= ' + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)])
		return render(request, 'postsong.html', {'NearPlaces' : resNearPlaces})

@login_required(login_url='/')
def plus(request):
	return render(request, 'plus.html')

@login_required(login_url='/')
def songpostpointadd(request):
	if request.is_ajax():
		if request.method == 'POST':
			songID = request.POST['SongPoint_SongPostID']
			userID = request.POST['SongPoint_User']

			song = SongPost.objects.get(pk=songID)
			user = User.objects.get(pk=userID)

			songPoint = SongPoint(SongPoint_SongPostID=song, SongPoint_User=user)
			songPoint.save()

			respuesta = {'codigo': 1, 'msg': 'Se ha guardado el voto.'}
			return HttpResponse(json.dumps(respuesta))

@login_required(login_url='/')
def songpostpointdel(request):
	if request.is_ajax():
		if request.method == 'POST':
			songID = request.POST['SongPoint_SongPostID']
			userID = request.POST['SongPoint_User']

			song = SongPost.objects.get(pk=songID)
			user = User.objects.get(pk=userID)

			songPoint = SongPoint.objects.get(SongPoint_SongPostID=song, SongPoint_User=user)
			songPoint.delete()

			respuesta = {'codigo': 2, 'msg': 'Se ha eliminado el voto.'}
			return HttpResponse(json.dumps(respuesta))

def getplaces(request):
	resPlaces = Place.objects.all()
	lstLugares = []
	for lugar in resPlaces:
		dctLugares = {
		"PlaceID":lugar.PlaceID,
		"PlaceName":lugar.PlaceName,
		"PlaceLat":lugar.PlaceLat,
		"PlaceLong":lugar.PlaceLong,
		}
		lstLugares.append(dctLugares) 

	respuesta = {"data":lstLugares}
	return HttpResponse(json.dumps(respuesta), content_type='application/json')

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

	resPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= '  + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)])[:10]

	#resPersonas = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= ' + str(qLatMin) + ' AND PlaceLong >= ' + str(qLongMax) + ' AND PlaceLong <= ' + str(qLongMin)]).filter(photopost__PhotoPostDateTime__range=[hoy, manana]).annotate(tPersonas=Count('photopost__PhotoPostID'))[:10]

	lstPlacePhotos = []

	for dPlace in resPlaces:
		FotoObtenida = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID')[:1]
		totPersonas = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).Count()
		dctLugares = {
		"PlaceID":dPlace.PlaceID,
		"PlaceName":dPlace.PlaceName,
		"PlaceLat":dPlace.PlaceLat,
		"PlaceLong":dPlace.PlaceLong,
		"PlaceLogo":str(dPlace.PlaceLogo),
		"LastPhoto":str(FotoObtenida[0].PhotoPostPhoto),
		"PeopleNow":totPersonas,
		}
		lstPlacePhotos.append(dctLugares)

	respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstPlacePhotos}
	return HttpResponse(json.dumps(respuesta), content_type='application/json')

def APIdataactivity(request):
	resUserActivity = PhotoPost.objects.select_related('user__userprofile').order_by('-PhotoPostID')

	lstActivity = []

	for act in resUserActivity:
		dctActivity = {
		'PhotoPhostID':act.PhotoPostID,
		'PhotoPostDateTime':act.PhotoPostDateTime.strftime('%Y-%m-%d %H:%M'),
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




	