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
from django.core.files.uploadedfile import SimpleUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.mail import EmailMessage
import foursquare
import json


def index(request):
	# if not request.user.is_anonymous():
	# 	return HttpResponseRedirect('/home/')
	# else:
	# 	loginForm = AuthenticationForm()
	# 	return render(request, 'login.html', {'loginForm' : loginForm})
	# 	#return (HttpResponseRedirect('/admin/'))
	return render(request, 'tienda.html')

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
	qLat = request.GET.get('qLat', False)
	qLong = request.GET.get('qLong', False)
	

	#Sumamos los valores del marge de error
	qLatMax = float(qLat) + 0.0030000
	qLatMin = float(qLat) - 0.0030000

	qLongMax = float(qLong) + 0.0030000
	qLongMin = float(qLong) - 0.0030000
	
	#resPlaces = Place.objects.all()
	resPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= '  + str(qLatMin) + ' AND PlaceLong <= ' + str(qLongMax) + ' AND PlaceLong >= ' + str(qLongMin)])[:10]

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

	resPlaces = Place.objects.extra(where=['PlaceLat <= ' + str(qLatMax) + ' AND PlaceLat >= '  + str(qLatMin) + ' AND PlaceLong <= ' + str(qLongMax) + ' AND PlaceLong >= ' + str(qLongMin)])[:10]

	#resPlaces = Place.objects.all()[:10]


	lstPlacePhotos = []

	for dPlace in resPlaces:
		hayFoto = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID').count()
		if hayFoto > 0:
			FotoObtenida = PhotoPost.objects.filter(PhotoPost_PlaceID=dPlace).order_by('-PhotoPostID')[:1]
			laFoto = str(FotoObtenida[0].PhotoPostPhoto)
			laFecha = str(FotoObtenida[0].PhotoPostDateTime)
		else:
			laFoto = 'nofoto.jpg'
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

@csrf_exempt
def APIsavephotopost(request):
	if request.method == 'POST':
		formPhotoPost = PhotoPostForm(request.POST, request.FILES)
		if formPhotoPost.is_valid():
			u = formPhotoPost.save(commit=False)
			u.PhotoPostDateTime = datetime.now()
			u.save()
			#return HttpResponseRedirect('/')
			return HttpResponse("Photopost has been succesfully uploaded.")
		else:
			#return HttpResponseRedirect('/novalid/')
			return HttpResponse("Error during upload.")
	else:
		#return HttpResponseRedirect('/nopost/')
		return HttpResponse("El request no es del tipo POST.")

@csrf_exempt
def APIsaveplace(request):
	if request.method == 'POST':
		p = Place(PlaceName=request.POST['PlaceName'], PlaceLat=request.POST['PlaceLat'], PlaceLong=request.POST['PlaceLong'])
		p.save()
		return HttpResponse("Se ha guardado correctamente el nuevo lugar.")
	else:
		return HttpResponse("El request no es post.")

@csrf_exempt
def APIloginpartyon(request):
	loginForm = AuthenticationForm()
	usuario = request.GET.get('username', False)
	clave = request.GET.get('password', False)
	acceso = authenticate(username=usuario, password=clave)
	if acceso is not None:
		login(request, acceso)
		respuesta = {'codigo': 1, 'msg': 'Welcome to partyon', 'data':[{'UIdPOChHnApi':acceso.id, 'username':acceso.username}]}
		return HttpResponse(json.dumps(respuesta))
		#return HttpResponseRedirect('/')
	else:
		respuesta = {'codigo': 2, 'msg': 'You have entered an incorrect email or password.', 'data':[{'UIdPOChHnApi':0, 'username':'error_No_Login_POChHn'}]}
		return HttpResponse(json.dumps(respuesta))
		#return render(request, 'login.html', {'loginForm' : loginForm})

def APIuserprofile(request):
	UserID = request.GET.get('uid', False)

	perfil = UserProfile.objects.filter(UserProfileID=UserID)

	hayFoto = PhotoPost.objects.filter(PhotoPost_User=perfil).order_by('-PhotoPostID').count()
	if hayFoto > 0:
		FotoObtenida = PhotoPost.objects.filter(PhotoPost_User=perfil).order_by('-PhotoPostID')[:1]
		laFoto = str(FotoObtenida[0].PhotoPostPhoto)
		laFecha = str(FotoObtenida[0].PhotoPostDateTime)
	else:
		laFoto = 'nofoto.jpg'
		laFecha = "No Data"

	resUserActivity = PhotoPost.objects.filter(PhotoPost_User=perfil).select_related('user__userprofile').order_by('-PhotoPostID')[:10]

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


	lstPerfil = []
	dctPerfil = {
	'UserProfileID':perfil[0].UserProfileID,
	'first_name':perfil[0].UserProfile_User.first_name + ' ' + perfil[0].UserProfile_User.last_name,
	'last_name':perfil[0].UserProfile_User.last_name,
	'email':perfil[0].UserProfile_User.email,
	'username':perfil[0].UserProfile_User.username,
	'userID':perfil[0].UserProfile_User.id,
	'photo':str(perfil[0].UserProfilePhoto),
	'email_verified':perfil[0].UserProfileMailVerified,
	'ultFotoTomada': laFoto,
	'ultFotoTomadaFecha':laFecha,
	}

	lstPerfil.append(dctPerfil)

	respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstPerfil, 'dataActivity':lstActivity}
	return HttpResponse(json.dumps(respuesta), content_type='application/json')

@csrf_exempt
def APIupdataphotoprofile(request):
	upf = UserProfileForm(request.POST, request.FILES)
	if request.method == 'POST':
		if upf.is_valid():
			m = UserProfile.objects.get(pk=request.POST['UserProfileID'])
			m.UserProfilePhoto = request.FILES['UserProfilePhoto']
			m.save()
			return HttpResponse("Se ha actualizado correctamente la foto de perfil.")
		else:
			return HttpResponse(str(upf))
	else:
		return HttpResponse(str(upf))

@csrf_exempt
def APIupdatepasswords(request):
	try:
		usuario = request.GET.get('unamePOusertxtChangeHN', False)
		nuevaclave = request.GET.get('psswdPOuserpsswdChangeHNChActPO', False)

		u = User.objects.get(username__exact=usuario)
		u.set_password(nuevaclave)
		u.save()

		return HttpResponse("Se ha actualizado el password.")
	except Exception, e:
		return HttpResponse(e)

def APIheydj(request):
	qLat = request.GET.get('qLat', False)
	qLong = request.GET.get('qLong', False)

	#Sumamos los valores del marge de error
	qLatMax = float(qLat) + 0.0020000
	qLatMin = float(qLat) - 0.0020000

	qLongMax = float(qLong) + 0.0020000
	qLongMin = float(qLong) - 0.0020000

	resHeyDj = SongPost.objects.extra(where=['SongPostLat <= ' + str(qLatMax) + ' AND SongPostLat >= '  + str(qLatMin) + ' AND SongPostLong <= ' + str(qLongMax) + ' AND SongPostLong >= ' + str(qLongMin)])[:25]

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

@csrf_exempt
def APIsongpost(request):
	if request.method == 'POST':
		formSongPost = SongPostForm(request.POST)
		if formSongPost.is_valid():
			u = formSongPost.save(commit=False)
			u.SongPostDateTime = datetime.now()
			u.save()

			#VotarAuto = SongPoint(SongPoint_SongPostID=u, SongPoint_User=request.user)
			#VotarAuto.save()

			return HttpResponse("Se ha agregado correctamente la canción.")
		else:
			return HttpResponse("El formulario no es válido.")
	else:
		return HttpResponse("El método no es post.")

@csrf_exempt
def APIaddplace(request):
	if request.method == 'POST':
		formAddPlace = AddPlaceForm(request.POST)
		if formAddPlace.is_valid():
			u = formAddPlace.save(commit=False)
			u.save()
			return HttpResponse("Se ha agregado correctamente el nuevo lugar.")
		else:
			return HttpResponse("El formulario no es válido.")
	else:
		return HttpResponse("El método no es post.")

@csrf_exempt
def APIsignup(request):
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

			titulo = 'Welcome to PartyOn'
			contenido = 'Welcome to PartyOn\n'
			contenido += 'You need to confirm your email address in order to enjoy all the features of PartyOn, click on the link below to verify your email.\n'
			contenido += 'http://www.partyonapp.com/API/verify/email/?userProfcodeActivationclass=23das22das22d25&requestuidverifyEmail=' + str(ojUsuario.id) + '&markvalid=true'
			correo = EmailMessage(titulo, contenido, from_email='no_reply@partyonapp.com', to=[str(ojUsuario.email)])
			correo.send()

			return HttpResponse("Se ha agregado correctamente el nuevo usuairo.")
		else:
			return HttpResponse("Los datos no son validos.")
	else:
		return HttpResponse("")

def APIcomprobarusername(request):
	qUname = request.GET.get('uname', False)

	cantUsuarios = User.objects.filter(username=qUname)

	if cantUsuarios.count() > 0:
		respuesta = {'success':True, 'message':'ErrorUsername.', 'version':'v1', 'data':[{'Available':'False', 'error':'UserDuplicated'}]}
	else:
		respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':[{'Available':'True', 'error':'UserAcepted'}]}
	
	return HttpResponse(json.dumps(respuesta), content_type='application/json')


def APIcomprobaremail(request):
	qUemail = request.GET.get('uemail', False)

	cantEmails = User.objects.filter(email=qUemail)

	if cantEmails.count() > 0:
		respuesta = {'success':True, 'message':'ErrorEmail.', 'version':'v1', 'data':[{'Available':'False', 'error':'EmailDuplicated'}]}
	else:
		respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':[{'Available':'True', 'error':'EmailAcepted'}]}
	
	return HttpResponse(json.dumps(respuesta), content_type='application/json')

def APIget9photostiles(request):
	photos = PhotoPost.objects.all().order_by('-PhotoPostID')[:9]

	lstPhotos = []

	for photo in photos:
		dctPhoto = {
		"PhotoPostID":photo.PhotoPostID,
		"PhotoPostPhoto":str(photo.PhotoPostPhoto)
		}
		lstPhotos.append(dctPhoto)

	respuesta = {'success':True, 'message':'Success.', 'version':'v1', 'data':lstPhotos}
	return HttpResponse(json.dumps(respuesta), content_type='application/json')


def APIterms(request):
	return render(request, 'terms.html')

def APIprivacy(request):
	return render(request, 'privacy.html')

def APIverifyemail(request):
	uID = request.GET.get('requestuidverifyEmail', False)
	usuarioVerificar = UserProfile.objects.get(pk=uID)
	usuarioVerificar.UserProfileMailVerified = True
	usuarioVerificar.save()

	return HttpResponse("<h1>Se ha verificado tu email | PartyOn</h1>")

def APIsendvalidarcorreo(request):
	uID = request.GET.get('requestuidverifyEmail', False)

	usuario = UserProfile.objects.get(pk=uID)
	usuario2 = User.objects.get(pk=usuario.pk)

	titulo = 'Welcome to PartyOn'
	contenido = 'Welcome to PartyOn\n'
	contenido += 'You need to confirm your email address in order to enjoy all the features of PartyOn, click on the link below to verify your email.\n'
	contenido += 'http://www.partyonapp.com/API/verify/email/?userProfcodeActivationclass=23das22das22d25&requestuidverifyEmail=' + str(usuario.UserProfileID) + '&markvalid=true'
	correo = EmailMessage(titulo, contenido, from_email='no_reply@partyonapp.com', to=[str(usuario2.email)])
	correo.send()

	return HttpResponse("<h1>Se ha enviado tu email | PartyOn</h1>")


#Views to get data from foursquare
client = foursquare.Foursquare(client_id='1KXWI20YZCGJZJYLAWOJWAEYKN2D0P2X3SZBPZZTTVPFZYMU', client_secret='DDSQ4G0FKZXQOACGTVYFSDSU3ROB4FTLEAYNIDTUQUTLW3JV', redirect_uri='http://www.partyonapp.com/API/fsq/authorize/')

def fsqGetPlaces(request):
	# Build the authorization url for your app
	auth_uri = client.oauth.auth_url()

	return HttpResponseRedirect(auth_uri)

def fsqGetToken(request):
	tokenU = request.GET.get('code', False)

	# Interrogate foursquare's servers to get the user's access_token
	access_token = client.oauth.get_token(tokenU)

	# Apply the returned access token to the client
	client.set_access_token(access_token)

	# Get the user's data
	busqueda = client.venues(params={'near':'Choluteca,Honduras', 'query':'bar', 'limit':50, 'intent':'browse', 'radius':5000})

	return HttpResponse(str(busqueda))